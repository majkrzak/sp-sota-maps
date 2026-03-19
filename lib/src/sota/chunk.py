from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from .bbox import Bbox
from .helpers.cache import download

__all__ = ["Chunk"]

@dataclass
class Chunk:
    et: ET

    @classmethod
    def find(cls, bbox: Bbox) -> Self:

        left, bottom, right, top = bbox.t(4326).xyxy

        data = download(f"https://api.openstreetmap.org/api/0.6/map?bbox={left},{bottom},{right},{top}",
        f"{left}_{bottom}_{right}_{top}.osm")

        return Chunk(ET.parse(data))
