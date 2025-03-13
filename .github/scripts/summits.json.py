#!/usr/bin/env python
from sys import exit, stdout
from sota.summit import Summit
from sota.reference import Reference
from sota.gmina import Gmina
from sota.park import Park
from json import dump
from pyproj import Geod
from functools import partial


def serializer(obj):
    g = Geod("+ellps=WGS84")
    r2 = partial(round, ndigits=2)
    r4 = partial(round, ndigits=4)

    if isinstance(obj, Summit):
        return {
            "reference": obj.reference,
            "name": obj.name,
            "lat": r4(obj.lat),
            "lon": r4(obj.lon),
            "alt": r2(obj.alt),
            "gminas": obj.gminas,
            "parks": obj.parks,
            "insights": {
                "elevation": r2(obj.alt - obj.catalog_alt),
                "distance": r2(
                    g.line_length(
                        [r4(obj.lat), r4(obj.catalog_lat)],
                        [r4(obj.lon), r4(obj.catalog_lon)],
                    )
                ),
                "total_area": r2(abs(g.geometry_area_perimeter(obj.zone.shape)[0])),
                "polish_area": sum(
                    (
                        r2(abs(g.geometry_area_perimeter(gmina.shape)[0]))
                        for gmina in obj.gminas
                    )
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
