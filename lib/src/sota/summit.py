from dataclasses import dataclass, field
from typing import Self, Iterable, Optional
from pandas import DataFrame
from shapely import Point

from .helpers.fetch_summits import fetch_summits
from .zone import Zone
from .gmina import Gmina
from .park import Park
from .helpers.cache import pickled
from .reference import Reference


__all__ = ["Summit"]


class MetaSummit(type):
    SUMMITS: DataFrame = pickled("SUMMITS", fetch_summits)

    def __getitem__(cls, reference: Reference) -> Self:
        if f"{reference}" not in cls.SUMMITS.index:
            raise KeyError()

        return Summit(reference)

    def __iter__(cls) -> Iterable[Self]:
        for reference in cls.SUMMITS.index:
            yield Summit(Reference.from_str(reference))

    def __len__(cls) -> int:
        return len(cls.SUMMITS.index)


@dataclass
class Summit(metaclass=MetaSummit):

    reference: Reference
    _zone: Optional[Zone] = field(init=False, default=None)
    _peak: Optional[Point] = field(init=False, default=None)
    _gminas: Optional[list[Gmina]] = field(init=False, default=None)
    _parks: Optional[list[Park]] = field(init=False, default=None)

    @property
    def name(self) -> str:
        return (
            type(self).SUMMITS.loc[f"{self.reference}"].SummitName.split("(")[0].strip()
        )

    @property
    def lat(self) -> str:
        return self.zone.peak.y

    @property
    def lon(self) -> str:
        return self.zone.peak.x

    @property
    def alt(self) -> str:
        return self.zone.peak.z

    @property
    def catalog_lat(self) -> float:
        return type(self).SUMMITS.loc[f"{self.reference}"].Latitude

    @property
    def catalog_lon(self) -> float:
        return type(self).SUMMITS.loc[f"{self.reference}"].Longitude

    @property
    def catalog_alt(self) -> float:
        return type(self).SUMMITS.loc[f"{self.reference}"].AltM

    @property
    def zone(self) -> Zone:
        if self._zone is None:
            self._zone = pickled(
                f"{self.reference:slug}.zone",
                lambda: Zone.find(self.catalog_lat, self.catalog_lon, self.catalog_alt),
            )
        if self._zone is None:
            raise ValueError()
        return self._zone

    @property
    def peak(self) -> Point:
        if self._peak is None:
            self._peak = pickled(
                f"{self.reference:slug}.peak",
                lambda: self.zone.peak,
            )
        if self._peak is None:
            raise ValueError()
        return self._peak

    @property
    def gminas(self) -> list[Gmina]:
        if self._gminas is None:
            self._gminas = pickled(
                f"{self.reference:slug}.gminas",
                lambda: Gmina.find(self.zone.shape),
            )
        if self._gminas is None:
            raise ValueError()
        return self._gminas

    @property
    def parks(self) -> list[Park]:
        if self._parks is None:
            self._parks = pickled(
                f"{self.reference:slug}.parks",
                lambda: Park.find(self.zone.shape),
            )
        if self._parks is None:
            raise ValueError()
        return self._parks
