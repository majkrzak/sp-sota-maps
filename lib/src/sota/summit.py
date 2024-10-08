from dataclasses import dataclass, field
from typing import Self, Iterable, Optional
from pandas import DataFrame
from shapely import Point

from .helpers.fetch_summits import fetch_summits
from .zone import Zone
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
