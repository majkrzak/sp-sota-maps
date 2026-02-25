from dataclasses import dataclass
from functools import cache
from typing import ClassVar, Self

from geopandas import GeoDataFrame, read_file
from shapely import Geometry, Polygon

from .data import gminas_references
from .helpers.cache import download, pickled

__all__ = ["Gmina"]


class MetaGmina(type):
    @property
    @cache
    @lambda f: lambda x: pickled(f.__name__, lambda: f(x))
    def GMINAS(cls) -> GeoDataFrame:
        gminas = read_file(
            download(
                "https://mapy.geoportal.gov.pl/wss/service/PZGIK/PRG/WFS/AdministrativeBoundaries?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAME=A03_Granice_gmin",
                "A03_Granice_gmin.xml",
            ),
        )

        gminas = gminas[
            [
                "JPT_KOD_JE",
                "JPT_NAZWA_",
                "geometry",
            ]
        ]

        gminas = gminas.set_index("JPT_KOD_JE", drop=False)

        gminas = gminas.join(gminas_references)

        gminas = gminas.set_crs("EPSG:2180")
        gminas = gminas.to_crs("EPSG:4326")

        return gminas


@dataclass
class Gmina(metaclass=MetaGmina):
    EPSG: ClassVar[int] = 4326

    id: str
    name: str
    pga: str
    shape: Geometry

    @classmethod
    def find(cls, shape: Polygon) -> list[Self]:
        gminas = cls.GMINAS.copy()
        gminas.geometry = gminas.geometry.intersection(shape)
        gminas = gminas[~gminas.geometry.is_empty]

        assert (
            gminas.PGA.notna().all()
        ), f"{gminas[gminas.PGA.isna()].index.values} not in gminas.csv"

        return [
            Gmina(
                str(gmina.JPT_KOD_JE),
                str(gmina.JPT_NAZWA_),
                str(gmina.PGA),
                gmina.geometry,
            )
            for _, gmina in gminas.iterrows()
        ]
