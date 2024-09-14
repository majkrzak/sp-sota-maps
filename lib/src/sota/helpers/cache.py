from os import environ
from os.path import isfile, basename, join
from urllib.parse import urlparse
from requests import get
from zipfile import is_zipfile, ZipFile


CACHE_DIR = environ.get("SOTA_CACHE", "./cache")


def download(url):
    name = basename(urlparse(url).path)
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
