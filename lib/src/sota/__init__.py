from importlib.metadata import version, PackageNotFoundError
from os import environ
from logging import getLogger

try:
    __version__ = version("sp-sota-maps")
except PackageNotFoundError:
    pass

CACHE_DIR = environ.get("SOTA_CACHE", "./cache")
OUTPUT_DIR = environ.get("SOTA_OUTPUT", "./output")

LOGGER = getLogger(__name__)
