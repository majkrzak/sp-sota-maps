from dataclasses import dataclass
from pyproj import Geod, CRS, Transformer
from typing import Self
from math import floor, ceil
from shapely import Polygon, box

__all__ = ["Bbox"]


@dataclass
class Bbox:
    xl: float
    yl: float
    xh: float
    yh: float
    epsg: int

    @classmethod
    def new(cls, lat, lon, radius) -> Self:
        """Create Bbox around given coordinates and specified radius.
        Coordinates are given in WGS84 Latitude and Longitude and
        radius is given in meters.
        """
        geod = Geod("+ellps=WGS84")
        _, yh, _ = geod.fwd(lon, lat, 90 * 0, radius)
        xh, _, _ = geod.fwd(lon, lat, 90 * 1, radius)
        _, yl, _ = geod.fwd(lon, lat, 90 * 2, radius)
        xl, _, _ = geod.fwd(lon, lat, 90 * 3, radius)
        return Bbox(xl, yl, xh, yh, 4326)

    @property
    def xyxy(self):
        return self.xl, self.yl, self.xh, self.yh

    @property
    def xxyy(self):
        return self.xl, self.xh, self.yl, self.yh

    def t(self, epsg: int) -> Self:
        if epsg == self.epsg:
            return self

        t = Transformer.from_crs(
            CRS.from_epsg(self.epsg), CRS.from_epsg(epsg), always_xy=True
        ).transform
        xl, yl = t(self.xl, self.yl)
        xh, yh = t(self.xh, self.yh)
        return Bbox(xl, yl, xh, yh, epsg)

    def r(self) -> Self:
        return Bbox(
            floor(self.xl), floor(self.yl), ceil(self.xh), ceil(self.yh), self.epsg
        )

    def p(self) -> Polygon:
        return box(*self.xyxy)
