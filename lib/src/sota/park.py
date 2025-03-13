from dataclasses import dataclass
from typing import Self
from shapely import Polygon, Point
from owslib.wfs import WebFeatureService
from shapely.ops import transform
import geopandas as gpd
from geopandas import GeoDataFrame
from pandas import concat
from .bbox import Bbox
from .helpers.transformer import transformer
from .data import parks

__all__ = ["Park"]


@dataclass
class Park:
    name: str
    pota: str
    wwff: str

    @classmethod
    def find(self, shape: Polygon) -> list[Self]:

        TYPES = [
            "GDOS:ParkiNarodowe",
            "GDOS:ParkiKrajobrazowe",
            "GDOS:Rezerwaty",
            "GDOS:ObszaryChronionegoKrajobrazu",
            "GDOS:ZespolyPrzyrodniczoKrajobrazowe",
            "GDOS:ObszarySpecjalnejOchrony",
            "GDOS:SpecjalneObszaryOchrony",
            "GDOS:PomnikiPrzyrodyPowierzchniowe",
            "GDOS:UzytkiEkologiczne",
        ]

        WFS = WebFeatureService(
            url="https://sdi.gdos.gov.pl/wfs",
            version="1.1.0",
            # auth=Authentication(None, None, None, False),
        )

        def read_wfs(bbox):
            response = WFS.getfeature(
                typename=TYPES,
                bbox=bbox.t(2180).xyxy,
            )

            data = []
            for typ in TYPES:
                try:
                    data.append(gpd.read_file(response, layer=typ[5:]))
                except:
                    pass

            if not len(data):
                return GeoDataFrame(
                    {
                        "nazwa": ["otulina"],
                        "kodinspire": ["abs"],
                        "geometry": [Point(0, 0)],
                    }
                )
            else:
                return concat(data)

        data = read_wfs(Bbox.new(shape, 100))

        data.nazwa = data.nazwa.astype("str")
        data = data[~data.nazwa.str.endswith("otulina")]

        data = data[
            data.apply(
                lambda x: not transform(
                    transformer(4326, 2180).transform, shape
                ).disjoint(x.geometry),
                axis=1,
            )
        ]
        data = data.set_index("kodinspire", drop=False)
        data = data.join(parks, validate="one_to_one")

        assert data.FullName.notna().all()

        data = data.groupby(["FullName", "POTA", "WWFF"], sort=False).agg(
            {
                "FullName": "first",
                "POTA": "first",
                "WWFF": "first",
            }
        )
        return [
            Park(row["FullName"], row["POTA"], row["WWFF"])
            for _, row in data.iterrows()
        ]
