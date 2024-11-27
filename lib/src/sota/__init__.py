from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("sp-sota-maps")
except PackageNotFoundError:
    pass
