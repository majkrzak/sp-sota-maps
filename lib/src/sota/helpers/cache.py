from os import environ
from os.path import isfile, basename, join
from urllib.parse import urlparse
from requests import get
from zipfile import is_zipfile, ZipFile
from pickle import load, dump
from lzma import open

CACHE_DIR = environ.get("SOTA_CACHE", "./cache")


def download(url):
    name = f"{basename(urlparse(url).path)}.xz"
    path = join(CACHE_DIR, name)
    if not isfile(path):
        response = get(url)
        with open(path, "wb") as f:
            f.write(response.content)

    if is_zipfile(path):
        with ZipFile(path) as f:
            name = f.namelist()[0]
            path = join(CACHE_DIR, name)
            f.extract(name, CACHE_DIR)

    return open(path, "rb")


def pickled(name: str, ctor=None):
    path = join(CACHE_DIR, f"{name}.pickle.xz")
    if not isfile(path) and ctor is not None:
        obj = ctor()
        with open(path, "wb") as f:
            dump(obj, f)

    with open(path, "rb") as f:
        return load(f)
