from setuptools import setup, Extension
from pkgconfig import configure_extension

ext = Extension("sota.render_carto", ["src/sota/render_carto.cpp"])
configure_extension(ext, "libmapnik")

setup(ext_modules=[ext])
