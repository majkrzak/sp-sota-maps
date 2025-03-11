from pandas import read_csv
from importlib import resources

__all__ = ["parks", "gminas"]

with (resources.files() / "parks.csv").open("rt") as f:
    parks = read_csv(
        f,
        comment="#",
        index_col="kodinspire",
        keep_default_na=False,
        dtype="string",
    )

with (resources.files() / "gminas.csv").open("rt") as f:
    gminas = read_csv(
        f,
        comment="#",
        index_col="id",
        keep_default_na=False,
        dtype="string",
    )
