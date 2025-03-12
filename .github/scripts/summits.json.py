#!/usr/bin/env python
from sys import exit, stdout
from sota.summit import Summit
from sota.reference import Reference
from sota.gmina import Gmina
from sota.park import Park
from json import dump


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
                "lat_diff": round(obj.lat - obj.catalog_lat, 4),
                "lon_diff": round(obj.lon - obj.catalog_lon, 4),
                "alt_diff": round(obj.alt - obj.catalog_alt, 2),
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
    raise TypeError(f"{obj.__class__.__name__} is not JSON serializable")


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
