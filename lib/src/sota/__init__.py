from importlib.metadata import PackageNotFoundError, version
from logging import getLogger
from os import environ

try:
    __version__ = version("sp-sota-maps")
except PackageNotFoundError:
    pass

CACHE_DIR = environ.get("SOTA_CACHE", "./cache")
OUTPUT_DIR = environ.get("SOTA_OUTPUT", "./output")

LOGGER = getLogger(__name__)
