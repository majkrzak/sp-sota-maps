#! /usr/bin/env nix
#! nix shell github:majkrzak/sp-sota-maps#python --command python

from sys import exit, stdout

from sota.reference import Reference
from sota.summit import Summit


def main() -> int:

    print("# SP Activation Zones")
    print()
    print("> Calculated using 1 m resolution Digital Terrain Model (NMT) from the Head Office of Geodesy and Cartography (GUGiK), derived from LiDAR surveys (EVRF2007 vertical reference).")
    print()
    print("| Reference | Name | Tile(s) | Source(s) |")
    print("|-----------|------|---------|-----------|")

    for summit in [
        summit
        for summit in Summit
        if summit.reference.association == "SP"
    ]:
        ref: Reference = summit.reference
        symbols = ", ".join(summit.zone.hmap.symbols)
        reports = ", ".join(summit.zone.hmap.reports)
        print(f"| {ref} | {summit.name} | {symbols} | {reports} |")

    print("---")
    print()
    print("Built with `github:majkrzak/sp-sota-maps/scripts/sotlas.az.py`")

    return 0


if __name__ == "__main__":
    exit(main())
