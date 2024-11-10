from dataclasses import dataclass
from os import environ

OUTPUT_DIR = environ.get("SOTA_OUTPUT", "./output")


@dataclass
class Config:
    width: float
    height: float
    margin: float
