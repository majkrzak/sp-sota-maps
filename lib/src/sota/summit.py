from dataclasses import dataclass
from typing import ClassVar, Self, Iterable
from pandas import read_csv, DataFrame

from .helpers.fetch_summits import fetch_summits
from .zone import Zone
from .helpers.cache import download, pickled
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
        zone = pickled(
            f"{self.reference:slug}.zone",
            lambda: Zone.find(self.catalog_lat, self.catalog_lon, self.catalog_alt),
        )
        if zone is None:
            raise ValueError()
        return zone
