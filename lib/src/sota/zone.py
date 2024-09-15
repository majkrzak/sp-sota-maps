from dataclasses import dataclass
from typing import Self, Optional
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
    box,
)
from contourpy import contour_generator
from numpy import array, unravel_index, append
from numpy.ma import masked_array
from math import inf
import logging

REGION_RADIUS_PYRAMID = [256, 512, 1024, 2048, 4096]
ZONE_THRESHOLD = 25
EPSG = 2180


@dataclass
class Zone:

    hmap: Hmap
    peak: Point
    shape: Polygon

    @staticmethod
    def find(lat: float, lon: float) -> Optional[Self]:
        """Find the activation zone for given coordinates.
        Coordiates are given in WGS84.
        """

        for region_radius in REGION_RADIUS_PYRAMID:
            hmap = Hmap.find(Bbox.new(lat, lon, region_radius))
            data = hmap.data
            alt = data.max()
            y, x = unravel_index(data.argmax(), data.shape)

            contour = contour_generator(
                z=masked_array(data, mask=~(0 < data)),
                corner_mask=True,
                quad_as_tri=False,
                fill_type="ChunkCombinedOffsetOffset",
                chunk_count=(1, 1),
            ).filled(alt - ZONE_THRESHOLD, inf)

            if contour[0][0] is None:
                logging.error(
                    f"Invalid data, no contour found for {lat} {lon} at radius {region_radius}"
                )
                continue

            region = min(
                from_ragged_array(
                    GeometryType.POLYGON, contour[0][0], (contour[1][0], contour[2][0])
                ),
                key=lambda polygon: distance(Point(x, y), polygon),
            )

            lon, lat = transform(
                Point(x, y),
                lambda x: array(
                    transformer(2180, 4362).transform(*(hmap.transform * x.T))
                ).T,
            ).coords[0]

            if not region.within(box(10, 10, data.shape[1] - 10, data.shape[0] - 10)):
                logging.info(
                    f"No full coverage for {lat} {lon} at radius {region_radius}"
                )
                continue

            break

        return Zone(
            hmap,
            Point(lon, lat, alt),
            transform(
                region,
                lambda x: array(
                    transformer(2180, 4362).transform(*(hmap.transform * x.T))
                ).T,
            ),
        )
