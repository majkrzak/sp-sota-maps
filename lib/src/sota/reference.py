from dataclasses import dataclass
from typing import Self, ClassVar
from re import fullmatch, Pattern, compile


@dataclass
class Reference:
    PATTERN: ClassVar[Pattern[str]] = compile(
        r"(?P<association>[A-Z0-9]{2})/(?P<region>[A-Z0-9]{2})-(?P<id>[0-9]{3})"
    )

    association: str
    region: str
    id: int

    def __format__(self, format_spec: str) -> str:
        if format_spec == "":
            return f"{self.association}/{self.region}-{self.id:03}"
        elif format_spec == "slug":
            return f"{self.association}{self.region}{self.id:03}"

        raise ValueError()

    @classmethod
    def from_str(cls, reference: str) -> Self:
        match = fullmatch(cls.PATTERN, reference)
        if not match:
            raise ValueError()

        return Reference(
            match.group("association"),
            match.group("region"),
            int(match.group("id")),
        )
