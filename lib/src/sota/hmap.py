from dataclasses import dataclass
from typing import Self, Optional, ClassVar
from .bbox import Bbox
from owslib.wfs import WebFeatureService
from shapely import union_all
from .helpers.cache import download
import geopandas as gpd
from rasterio import open as rio_open
from rasterio.merge import merge as rio_merge
from affine import Affine
import numpy as np

__all__ = ["Hmap"]

YEARS = (2024, 2023, 2022, 2021, 2020, 2019, 2018)

WFS = WebFeatureService(
    "https://mapy.geoportal.gov.pl/wss/service/PZGIK/NumerycznyModelTerenuEVRF2007/WFS/Skorowidze",
    version="2.0.0",
)


def read_wfs(bbox, year):
    response = WFS.getfeature(
        typename=[f"gugik:SkorowidzNMT{year}"],
        bbox=bbox.t(2180).r().xyxy,
    )

    with open(f"data.xml", "wb") as f:
        f.write(response.read())

    try:
        return gpd.read_file("data.xml")
    except:
        return None


@dataclass
class Hmap:
    EPSG: ClassVar[int] = 2180

    data: np.array
    bounds: Bbox
    transform: Affine
    symbols: list[str]
    report: str

    @classmethod
    def find(cls, bbox: Bbox) -> Optional[Self]:
        """Find most recent height map data containing given bounding box."""
        for year in YEARS:
            data = read_wfs(bbox, year)
            if data is None:
                continue

            data = data[data.char_przestrz == "1.00 m"]
            data = data[data.format == "ARC/INFO ASCII GRID"]

            if data.empty:
                continue

            grouped = data.groupby(["blad_sr_wys", "nr_zglosz", "zrodlo_danych"])

            for _, group in grouped:
                if not bbox.t(cls.EPSG).p().covered_by(union_all(group.geometry)):
                    continue

                chunks = []
                for url in group.url_do_pobrania:
                    with download(url) as f:
                        chunk = rio_open(f, DATATYPE="Float64")
                        chunks.append(chunk)
                data, transform = rio_merge(chunks)

                xl, yh = transform * (0, 0)
                xh, yl = transform * (data.shape[2], data.shape[1])

                bounds = Bbox(xl, yl, xh, yh, cls.EPSG)

                return Hmap(
                    data[0, :, :],
                    bounds,
                    transform,
                    group.godlo.tolist(),
                    group.nr_zglosz[0],
                )
