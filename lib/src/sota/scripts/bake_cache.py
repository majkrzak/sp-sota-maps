from sys import exit

from ..summit import Summit


def main() -> int:
    return 0


if __name__ == "__main__":
    for summit in Summit:
        print(f"Generating for: {summit.reference}")
        print(summit.zone.peak)
