#! /usr/bin/env nix
#! nix shell github:majkrzak/sp-sota-maps#python --command python

from json import dump
from sys import exit, stdout

from geojson import Feature, FeatureCollection
from sota.summit import Summit


def main() -> int:
    dump(FeatureCollection([
        Feature(
            geometry=summit.zone.shape,
            properties={"Name": f"{summit.reference}"},
        )
        for summit in Summit
        if summit.reference.association == "SP"
    ]), stdout, ensure_ascii=False, separators=(",", ":"))

    return 0


if __name__ == "__main__":
    exit(main())
