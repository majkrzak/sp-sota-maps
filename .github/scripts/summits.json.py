#!/usr/bin/env python
from sys import exit, stdout
from sota.summit import Summit
from sota.reference import Reference
from sota.gmina import Gmina
from sota.park import Park
from json import dump
from pyproj import Geod


def serializer(obj):
    if isinstance(obj, Summit):
        return {
            "reference": obj.reference,
            "name": obj.name,
            "lat": round(obj.lat, 4),
            "lon": round(obj.lon, 4),
            "alt": round(obj.alt, 2),
            "gminas": obj.gminas,
            "parks": obj.parks,
            "insights": {
                "elevation": round(obj.alt - obj.catalog_alt, 2),
                "distance": round(
                    Geod("+ellps=WGS84").line_length(
                        [round(obj.lat, 4), round(obj.catalog_lat, 4)],
                        [round(obj.lon, 4), round(obj.catalog_lon, 4)],
                    ),
                    2,
                ),
            },
            "hmap": {
                "symbols": obj.zone.hmap.symbols,
                "reports": obj.zone.hmap.reports,
            },
        }
    if isinstance(obj, Reference):
        return f"{obj}"
    if isinstance(obj, Gmina):
        return {
            "name": obj.name,
            "pga": obj.pga,
        }
    if isinstance(obj, Park):
        return {
            "name": obj.name,
            "pota": obj.pota,
            "wwff": obj.wwff,
        }
    raise TypeError(f"{obj.__class__.__name__} {obj} is not JSON serializable")


def main() -> int:

    dump(
        list(Summit),
        stdout,
        default=serializer,
        ensure_ascii=False,
        indent=2,
    )

    return 0


if __name__ == "__main__":
    exit(main())
