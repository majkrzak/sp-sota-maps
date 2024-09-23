from pandas import read_csv

from .cache import download


def fetch_summits():
    summits = read_csv(
        download("https://storage.sota.org.uk/summitslist.csv"),
        low_memory=False,
        skiprows=[0],
        header=0,
        index_col=0,
    )

    # Select covered summits
    summits = summits[
        (summits.AssociationName == "Poland")
        | (
            summits.index.isin(
                [  # border summits (maybe auto based on distance?)
                    "OK/LI-003",
                    "OK/KR-001",
                    # "OK/OL-011", # Partially in Poland, no height data for peak available
                    "OK/OL-022",
                    "OK/MO-061",
                    "OM/ZA-045",
                    "OM/ZA-059",
                    "OM/ZA-061",
                    "OM/ZA-023",
                    "OM/ZA-046",
                    "OM/ZA-081",
                    "OM/ZA-005",
                    "OM/PO-012",
                    "OM/PO-054",
                    "OM/PO-013",
                    "OM/PO-092",
                    "OM/PO-040",
                    # "UT/CA-189", # Partially in Poland, no height data for peak available
                    # "UT/CA-234", # Border peek, part of zone height data missing
                ]
            )
        )
    ]

    # Remove invalid summits
    summits = summits[summits.ValidTo == "31/12/2099"]

    # Clean unnecessary columns
    summits = summits.drop(
        columns=[
            "AltFt",
            "GridRef1",
            "GridRef2",
            "ValidFrom",
            "ValidTo",
            "ActivationCount",
            "ActivationDate",
            "ActivationCall",
        ]
    )

    return summits
