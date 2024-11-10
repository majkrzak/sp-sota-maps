from dataclasses import dataclass
from typing import Self
from math import floor, ceil

from ..bbox import Bbox
from ..summit import Summit


@dataclass
class ViewPort:
    width: float
    height: float
    bbox: Bbox
    scale: int

    @property
    def epsg(self) -> int:
        return self.bbox.epsg

    @property
    def figsize(self) -> (float, float):
        M2I = 39.3700787
        return (self.width * M2I, self.height * M2I)

    @classmethod
    def new(
        cls,
        width: float,  # Paper width in meters
        height: float,  # Paper width in meters
        min_margin: float,
        summit: Summit,
    ) -> Self:
        """Builds ViewBox for landscape page in 2/3 layout."""

        bbox = Bbox.new(summit.zone.shape, 0)
        lon = bbox.p().centroid.x

        max_radius = min(width, height) - 2 * min_margin

        for scale in [500, 1000, 2000, 5000, 10000, 25000]:
            epsg = pick_epsg(lon, scale)
            if bbox.t(epsg).absolute_radius / scale < max_radius:
                break

        return ViewPort(
            width, height, scaled_bobx(bbox.t(epsg), width, height, scale), scale
        )


def scaled_bobx(bbox: Bbox, width: float, height: float, scale: int) -> Bbox:
    """Build scaled bounding box, with oryhinal placed in right 2 thirds of page"""
    x, y = bbox.p().centroid.x, bbox.p().centroid.y
    x, y = round(x), round(y)
    dx = floor((width * scale) / 2)
    dy = ceil((height * scale) / 2)
    xl = x - dx - (dx - dy)
    xh = x + dx - (dx - dy)
    yh = y + dy
    yl = y - dy
    return Bbox(xl, yl, xh, yh, bbox.epsg)


def pick_epsg(lon: float, scale: int) -> int:
    """Pick correct terrestrial reference system.
    In Poland for scales lower or equal 10000, PL_UTM is used.
    Otherwise, for more detailed studies, PL-2000.
    """
    if scale >= 10000:
        if 12 < lon < 18:
            return 32633
        if 18 < lon < 24:
            return 32634
        if 24 < lon < 30:
            return
    if scale < 10000:
        if lon < 16.5:
            return 2176
        if 16.5 < lon < 19.5:
            return 2177
        if 19.5 < lon < 22.5:
            return 2178
        if 22.5 < lon:
            return 2179
