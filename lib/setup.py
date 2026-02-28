from os import environ

from pkgconfig import configure_extension, variables
from setuptools import Extension, setup

ext = Extension("sota.render_carto", ["src/sota/render_carto.cpp"])
configure_extension(ext, "libmapnik")
ext.define_macros.append(
    ("MAPNIK_PLUGINDIR", '"' + variables("libmapnik")["plugins_dir"] + '"')
)

setup(ext_modules=[ext], version=environ.get("version"))
