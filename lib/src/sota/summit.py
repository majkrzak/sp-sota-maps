from dataclasses import dataclass, field
from typing import Self, Iterable, Optional
from pandas import DataFrame, read_csv
from shapely import Point
from functools import cache
from .zone import Zone
from .gmina import Gmina
from .park import Park
from .helpers.cache import pickled, download
from .reference import Reference


__all__ = ["Summit"]


class MetaSummit(type):
    @property
    @cache
    @lambda f: lambda x: pickled(f.__name__, lambda: f(x))
    def SUMMITS(cls) -> DataFrame:
        summits = read_csv(
            download("https://storage.sota.org.uk/summitslist.csv"),
            low_memory=False,
            skiprows=[0],
            index_col=0,
        )

        # Select covered summits
        summits = summits[
            (summits.AssociationName == "Poland")
            | (
                summits.index.isin(
                    [  # border summits (maybe auto based on distance?)
                        # "OK/LI-003", # Partially in Poland, no height data for one of the peaks available
                        "OK/KR-001",
                        # "OK/OL-011", # Partially in Poland, no height data for peak available
                        "OK/OL-022",
                        "OK/MO-061",
                        "OM/ZA-045",
                        "OM/ZA-059",
                        "OM/ZA-061",
                        "OM/ZA-023",
                        "OM/ZA-046",
                        "OM/ZA-081",
                        "OM/ZA-005",
                        "OM/PO-012",
                        "OM/PO-054",
                        "OM/PO-013",
                        "OM/PO-092",
                        "OM/PO-040",
                        # "UT/CA-189", # Partially in Poland, no height data for peak available
                        # "UT/CA-234", # Border peek, part of zone height data missing
                    ]
                )
            )
        ]

        # Remove invalid summits
        summits = summits[summits.ValidTo == "31/12/2099"]

        # Clean unnecessary columns
        summits = summits[
            [
                "SummitName",
                "Latitude",
                "Longitude",
                "AltM",
            ]
        ]

        # Set datatypes
        summits.SummitName = summits.SummitName.astype(str)
        summits.Latitude = summits.Latitude.astype(float)
        summits.Longitude = summits.Longitude.astype(float)
        summits.AltM = summits.AltM.astype(float)

        return summits

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
