from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from .bbox import Bbox
from .helpers.cache import download

__all__ = ["Chunk"]

@dataclass(eq=True, order=True, frozen=True)
class Tag:
    k: str
    v: str

    @classmethod
    def from_xml(cls, e: ET.Element) -> Self:
        k = e.attrib["k"]
        v = e.attrib["v"]

        return Tag(k,v)

    def to_xml(self) -> ET.Element:
        return ET.Element("tag", k=self.k, v=self.v)


@dataclass(eq=True, order=True, frozen=True)
class Node:
    id: int
    visible: bool
    lat: float
    lon: float
    tags: tuple[Tag]

    @classmethod
    def from_xml(cls, e: ET.Element) -> Self:
        id = int(e.attrib["id"])
        visible = e.attrib["visible"] != "false"
        lat = float(e.attrib["lat"])
        lon = float(e.attrib["lon"])
        tags = tuple(Tag.from_xml(t) for t in e.iter("tag"))

        return Node(id, visible, lat, lon, tags)

    def to_xml(self) -> ET.Element:
        e = ET.Element("node", id=str(self.id), visible="true" if self.visible else "false", lat=str(self.lat), lon=str(self.lon))
        e.extend(tag.to_xml() for tag in self.tags)
        return e

@dataclass(eq=True, order=True, frozen=True)
class Nd:
    ref: int

    @classmethod
    def from_xml(cls, e: ET.Element) -> Self:
        ref = int(e.attrib["ref"])

        return Nd(ref)

    def to_xml(self) -> ET.Element:
        return ET.Element("nd", ref=str(self.ref))

@dataclass(eq=True, order=True, frozen=True)
class Way:
    id: int
    visible: bool
    nodes: tuple[int]
    tags: tuple[Tag]

    @classmethod
    def from_xml(cls, e: ET.Element) -> Self:
        id = int(e.attrib["id"])
        visible = e.attrib["visible"] != "false"
        nodes = tuple(Nd.from_xml(n) for n in e.iter("nd"))
        tags = tuple(Tag.from_xml(t) for t in e.iter("tag"))

        return Way(id, visible, nodes, tags)

    def to_xml(self) -> ET.Element:
        e = ET.Element("way", id=str(self.id), visible="true" if self.visible else "false")
        e.extend(node.to_xml() for node in self.nodes)
        e.extend(tag.to_xml() for tag in self.tags)
        return e

@dataclass(eq=True, order=True, frozen=True)
class Member:
    type: str
    ref: int
    role: str

    @classmethod
    def from_xml(cls, e: ET.Element) -> Self:
        type = str(e.attrib["type"])
        ref = int(e.attrib["ref"])
        role = str(e.attrib["role"])

        return Member(type, ref, role)

    def to_xml(self) -> ET.Element:
        return ET.Element("member", type=self.type, ref=str(self.ref), role=self.role)

@dataclass(eq=True, order=True, frozen=True)
class Relation:
    id: int
    visible: bool
    members: tuple[Member]
    tags: tuple[Tag]

    @classmethod
    def from_xml(cls, e: ET.Element) -> Self:
        id = int(e.attrib["id"])
        visible = e.attrib["visible"] != "false"
        members = tuple(Member.from_xml(n) for n in e.iter("member"))
        tags = tuple(Tag.from_xml(t) for t in e.iter("tag"))

        return Relation(id, visible, members, tags)

    def to_xml(self) -> ET.Element:
        e = ET.Element("relation", id=str(self.id), visible="true" if self.visible else "false")
        e.extend(member.to_xml() for member in self.members)
        e.extend(tag.to_xml() for tag in self.tags)
        return e


@dataclass
class Chunk:
    nodes: tuple[Node]
    ways: tuple[Way]
    relations: tuple[Relation]


    @classmethod
    def find(cls, bbox: Bbox) -> Self:

        left, bottom, right, top = bbox.t(4326).xyxy

        data = download(f"https://api.openstreetmap.org/api/0.6/map?bbox={left},{bottom},{right},{top}",
        f"{left}_{bottom}_{right}_{top}.osm")

        return Chunk.from_xml(ET.parse(data).getroot())


    @classmethod
    def from_xml(cls, e: ET.Element) -> Self:
        nodes = tuple(Node.from_xml(n) for n in e.iter("node"))
        ways = tuple(Way.from_xml(w) for w in e.iter("way"))
        relations = tuple(reversed(tuple(Relation.from_xml(r) for r in e.iter("relation"))))

        return Chunk(nodes,ways,relations)

    def to_xml(self) -> ET.Element:
        e = ET.Element("osm", version="0.6")
        e.extend(node.to_xml() for node in self.nodes)
        e.extend(way.to_xml() for way in self.ways)
        e.extend(relation.to_xml() for relation in reversed(self.relations))
        return e

    def __add__(self, other: Self) -> Self:
        """Merge with another chunk, preserving order."""

        def _merge(lhs, rhs, *, rev=False):
            i,j = 0,0

            while i < len(lhs) and j < len(rhs):
                a, b = lhs[i], rhs[j]

                if a < b:
                    if not rev:
                        yield a
                        i += 1
                    else:
                        yield b
                        j += 1
                elif b < a:
                    if not rev:
                        yield b
                        j += 1
                    else:
                        yield a
                        i += 1
                else:
                    yield a
                    i += 1
                    j += 1

            yield from lhs[i:]
            yield from rhs[j:]


        nodes = tuple(_merge(self.nodes, other.nodes))
        ways = tuple(_merge(self.ways, other.ways))
        relations = tuple(_merge(self.relations, other.relations, rev=True))
        return Chunk(nodes, ways, relations)

