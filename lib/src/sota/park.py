from dataclasses import dataclass
from functools import cache
from typing import Self

from geopandas import GeoDataFrame, list_layers, read_file
from pandas import concat
from shapely import Geometry, Polygon, union_all

from .data import parks_references
from .helpers.cache import download, pickled

__all__ = ["Park"]


class MetaPark(type):
    @property
    @cache
    @lambda f: lambda x: pickled(f.__name__, lambda: f(x))
    def PARKS(cls) -> GeoDataFrame:

        file = download(
            "https://sdi.gdos.gov.pl/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAME=GDOS:ParkiNarodowe,GDOS:ParkiKrajobrazowe,GDOS:Rezerwaty,GDOS:ObszaryChronionegoKrajobrazu,GDOS:ZespolyPrzyrodniczoKrajobrazowe,GDOS:ObszarySpecjalnejOchrony,GDOS:SpecjalneObszaryOchrony,GDOS:PomnikiPrzyrodyPowierzchniowe,GDOS:UzytkiEkologiczne",
            "gdos_parks.xml",
        )

        parks = concat(
            [read_file(file, layer=layer) for layer in list_layers(file).name]
        )

        parks = parks[~parks.nazwa.astype("str").str.endswith("otulina")]

        parks = parks[
            [
                "kodinspire",
                "geometry",
            ]
        ]

        parks = parks.set_index("kodinspire", drop=False)

        parks = parks.join(parks_references)

        parks = parks.set_crs("EPSG:2180")
        parks = parks.to_crs("EPSG:4326")

        return parks


@dataclass
class Park(metaclass=MetaPark):
    name: str
    pota: str
    wwff: str
    shape: Geometry

    @classmethod
    def find(cls, shape: Polygon) -> list[Self]:
        parks = cls.PARKS.copy()
        parks.geometry = parks.geometry.intersection(shape)
        parks = parks[~parks.geometry.is_empty]

        assert (
            parks.full_name.notna().all()
        ), f"{parks[parks.full_name.isna()].index.values} not in parks.csv"

        parks = parks.groupby(["full_name", "POTA", "WWFF"], sort=False).agg(
            {
                "full_name": "first",
                "POTA": "first",
                "WWFF": "first",
                "geometry": union_all,
            }
        )

        parks = parks[parks.full_name.ne("") & (parks.POTA.ne("") | parks.WWFF.ne(""))]

        return [
            Park(
                str(park.full_name),
                str(park.POTA),
                str(park.WWFF),
                park.geometry,
            )
            for _, park in parks.iterrows()
        ]
