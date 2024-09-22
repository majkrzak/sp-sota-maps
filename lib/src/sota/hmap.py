from dataclasses import dataclass
from typing import Self, Optional, ClassVar

from geopandas import GeoDataFrame

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

    data: np.ndarray[np.float64]
    bounds: Bbox
    transform: Affine
    symbols: list[str]
    reports: list[str]

    @classmethod
    def find(cls, bbox: Bbox) -> Optional[Self]:
        """Find most recent height map data containing given bounding box."""

        def _build_zone(frame: GeoDataFrame) -> Optional[Self]:
            if not bbox.t(cls.EPSG).p().covered_by(union_all(frame.geometry)):
                return None

            chunks = []
            for url in frame.url_do_pobrania:
                with download(url) as f:
                    chunk = rio_open(f, driver="AAIGrid", DATATYPE="Float64")
                    chunks.append(chunk)
            data, transform = rio_merge(chunks)

            xl, yh = transform * (0, 0)
            xh, yl = transform * (data.shape[2], data.shape[1])

            bounds = Bbox(xl, yl, xh, yh, cls.EPSG)

            return Hmap(
                data[0, :, :],
                bounds,
                transform,
                frame.godlo.tolist(),
                frame.nr_zglosz.tolist(),
            )

        for year in YEARS:
            index = read_wfs(bbox, year)
            if index is None:
                continue

            index = index[index.char_przestrz == "1.00 m"]
            index = index[index.format == "ARC/INFO ASCII GRID"]

            if index.empty:
                continue

            for _, group in index.groupby(["blad_sr_wys", "blad_sr_syt", "nr_zglosz"]):
                zone = _build_zone(group)
                if zone is None:
                    continue
                return zone

            for _, group in index.groupby(
                ["blad_sr_wys", "blad_sr_syt", "zrodlo_danych"]
            ):
                zone = _build_zone(group)
                if zone is None:
                    continue
                return zone

            for _, group in index.groupby(["zrodlo_danych"]):
                zone = _build_zone(group)
                if zone is None:
                    continue
                return zone
