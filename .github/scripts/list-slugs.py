#!/usr/bin/env python
from sota.summit import Summit


def main() -> int:
    print(*(f"{summit.reference:slug}" for summit in Summit), sep=" ", end="")
    return 0


if __name__ == "__main__":
    exit(main())
