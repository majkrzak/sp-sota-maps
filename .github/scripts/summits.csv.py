#!/usr/bin/env python
from sys import exit, stdout
from csv import writer
from sota.summit import Summit


def main() -> int:

    w = writer(stdout)

    w.writerow(
        [
            "reference",
            "name",
            "lat",
            "lon",
            "alt",
        ]
    )

    for summit in Summit:
        w.writerow(
            [
                f"{summit.reference}",
                summit.name,
                summit.lat,
                summit.lon,
                summit.alt,
            ]
        )

    return 0


if __name__ == "__main__":
    exit(main())
