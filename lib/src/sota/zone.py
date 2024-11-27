from dataclasses import dataclass
from typing import Self, Optional, ClassVar
from .hmap import Hmap
from .bbox import Bbox
from .helpers.transformer import transformer
from shapely import (
    Polygon,
    Point,
    transform,
    distance,
    from_ragged_array,
    GeometryType,
)
from contourpy import contour_generator
from numpy import array, unravel_index, round
from numpy.ma import masked_array
from math import inf
from rasterio.features import rasterize

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

__all__ = ["Zone"]

REGION_MARGIN = 16
ZONE_THRESHOLD = 25


@dataclass
class Zone:
    EPSG: ClassVar[int] = 4326

    shape: Polygon
    peak: Point
    hmap: Hmap

    @classmethod
    def find(cls, lat: float, lon: float, alt: float) -> Optional[Self]:
        """Find the activation zone for given coordinates.
        Coordinates are given in WGS84.
        """

        def _hmap(zone: Polygon | Point) -> Optional[Hmap]:
            logger.info("Generating hmap for zone")
            return Hmap.find(Bbox.new(zone, REGION_MARGIN))

        def _zone(peak: Point, hmap: Hmap) -> Optional[Polygon]:
            logger.info(f"Generating zone for: {peak}")

            def to_xy(p):
                return array(
                    ~hmap.transform
                    * array(transformer(Zone.EPSG, hmap.EPSG).transform(*p.T))
                ).T

            def from_xy(p):
                return array(
                    transformer(hmap.EPSG, cls.EPSG).transform(*(hmap.transform * p.T))
                ).T

            x, y = round(transform(peak, to_xy).coords[0])

            contour = contour_generator(
                z=masked_array(hmap.data, mask=~(0 < hmap.data)),
                corner_mask=True,
                quad_as_tri=False,
                fill_type="ChunkCombinedOffsetOffset",
                chunk_count=(1, 1),
            ).filled(peak.z - ZONE_THRESHOLD, inf)

            if contour[0][0] is None:
                return None

            region = min(
                from_ragged_array(
                    GeometryType.POLYGON, contour[0][0], (contour[1][0], contour[2][0])
                ),
                key=lambda polygon: distance(Point(x, y), polygon),
            )

            return transform(region, from_xy)

        def _peak(zone: Polygon, hmap: Hmap) -> Point:
            logger.info("Searching peak in zone")

            def to_xy(p):
                return array(
                    ~hmap.transform
                    * array(transformer(Zone.EPSG, hmap.EPSG).transform(*p.T))
                ).T

            def from_xy(p):
                return array(
                    transformer(hmap.EPSG, cls.EPSG).transform(*(hmap.transform * p.T))
                ).T

            zone_data = masked_array(
                hmap.data,
                mask=(
                    rasterize(
                        [transform(zone, to_xy)], out_shape=hmap.data.shape, fill=0
                    )
                    == 0
                ),
            )

            y, x = unravel_index(zone_data.argmax(), zone_data.shape)
            z = zone_data[y, x]

            return Point(*transform(Point(x, y), from_xy).coords[0], z)

        def _find(peak: Point, zone: Polygon | Point) -> Optional[Zone]:

            hmap = _hmap(zone)
            if hmap is None:
                logger.error("Hmap not found!")
                return

            new_zone = _zone(peak, hmap)
            if new_zone is None:
                logger.error("Zone not found!")
                return

            new_peak = _peak(new_zone, hmap)
            if new_peak is None:
                logger.error("Peak not found!")
                return

            if new_peak != peak or new_zone != zone:
                return _find(new_peak, new_zone)

            return Zone(zone, peak, hmap)

        init = Point(lon, lat, alt)

        return _find(init, init)
