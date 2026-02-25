from importlib import resources

from pandas import read_csv

__all__ = ["parks_references", "gminas_references"]

with (resources.files() / "parks.csv").open("rt") as f:
    parks_references = read_csv(
        f,
        comment="#",
        index_col="kodinspire",
        keep_default_na=False,
        dtype="string",
    )

with (resources.files() / "gminas.csv").open("rt") as f:
    gminas_references = read_csv(
        f,
        comment="#",
        index_col="id",
        keep_default_na=False,
        dtype="string",
    )
