from setuptools import setup, Extension

ext = Extension("sota.render_carto", ["src/sota/render_carto.cpp"])

ext.define_macros.extend([("HAVE_CAIRO", None)])
ext.libraries.extend(["mapnik"])

setup(ext_modules=[ext])
