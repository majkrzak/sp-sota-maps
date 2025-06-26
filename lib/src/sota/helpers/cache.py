from os.path import isfile, basename, join
from urllib.parse import urlparse
from requests import get
from pickle import load, dump
from lzma import open
from .. import CACHE_DIR


def download(url, name=None):
    path = join(CACHE_DIR, f"{name or basename(urlparse(url).path)}.xz")
    if not isfile(path):
        response = get(url)
        with open(path, "wb") as f:
            f.write(response.content)

    return open(path, "rb")


def pickled(name: str, ctor=None):
    path = join(CACHE_DIR, f"{name}.pickle.xz")
    if not isfile(path) and ctor is not None:
        obj = ctor()
        with open(path, "wb") as f:
            dump(obj, f)

    with open(path, "rb") as f:
        return load(f)
