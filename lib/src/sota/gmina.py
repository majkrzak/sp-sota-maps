from dataclasses import dataclass
from typing import Self
from shapely import Polygon
from owslib.wfs import WebFeatureService
from shapely.ops import transform
import geopandas as gpd
from .bbox import Bbox
from .helpers.transformer import transformer
from .data import gminas

__all__ = ["Gmina"]

WFS = WebFeatureService(
    url="https://mapy.geoportal.gov.pl/wss/service/PZGIK/PRG/WFS/AdministrativeBoundaries",
    version="1.1.0",
)


def read_wfs(bbox):
    response = WFS.getfeature(
        typename=["A03_Granice_gmin"],
        bbox=bbox.t(2180).r().xyxy,
    )

    try:
        return gpd.read_file(response)
    except:
        return None


@dataclass
class Gmina:

    id: str
    name: str
    pga: str

    @classmethod
    def find(cls, shape: Polygon) -> list[Self]:

        data = read_wfs(Bbox.new(shape, 100))
        data = data[data["WAZNY_DO"].astype(str) == "0"]

        data = data[
            data.apply(
                lambda x: not transform(
                    transformer(4326, 2180).transform, shape
                ).disjoint(x.geometry),
                axis=1,
            )
        ]

        return [
            Gmina(
                str(row["JPT_KOD_JE"]),
                str(row["JPT_NAZWA_"]),
                str(gminas.PGA[str(row["JPT_KOD_JE"])]),
            )
            for _, row in data.iterrows()
        ]
