from dataclasses import dataclass

from pyproj import Geod, CRS, Transformer
from typing import Self
from math import floor, ceil
from shapely import box, Polygon
from shapely.geometry.base import BaseGeometry

__all__ = ["Bbox"]


@dataclass
class Bbox:
    xl: float
    yl: float
    xh: float
    yh: float
    epsg: int

    @classmethod
    def _new_coords(cls, lat: float, lon: float, radius: float) -> Self:
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

    @classmethod
    def _new_geometry(cls, geometry: BaseGeometry, radius: float) -> Self:
        """Create Bbox around given Polygon.
        Coordinates are given in WGS84 and
        radius is given in meters.
        """
        geod = Geod("+ellps=WGS84")
        w, s, e, n = geometry.bounds
        _, yh, _ = geod.fwd(e, n, 90 * 0, radius)
        xh, _, _ = geod.fwd(e, n, 90 * 1, radius)
        _, yl, _ = geod.fwd(w, s, 90 * 2, radius)
        xl, _, _ = geod.fwd(w, s, 90 * 3, radius)
        return Bbox(xl, yl, xh, yh, 4326)

    @classmethod
    def new(cls, *args) -> Self:
        if len(args) == 2 and isinstance(args[0], BaseGeometry):
            return cls._new_geometry(*args)

        if len(args) == 3 and isinstance(args[0], float) and isinstance(args[1], float):
            return cls._new_geometry(*args)

        raise TypeError()

    @property
    def xyxy(self):
        return self.xl, self.yl, self.xh, self.yh

    @property
    def xxyy(self):
        return self.xl, self.xh, self.yl, self.yh

    def t(self, epsg: int) -> Self:
        if epsg == self.epsg:
            return self

        transform = Transformer.from_crs(
            CRS.from_epsg(self.epsg), CRS.from_epsg(epsg), always_xy=True
        ).transform
        xl, yl = transform(self.xl, self.yl)
        xh, yh = transform(self.xh, self.yh)
        return Bbox(xl, yl, xh, yh, epsg)

    def r(self) -> Self:
        return Bbox(
            floor(self.xl), floor(self.yl), ceil(self.xh), ceil(self.yh), self.epsg
        )

    def p(self) -> Polygon:
        return box(*self.xyxy)
