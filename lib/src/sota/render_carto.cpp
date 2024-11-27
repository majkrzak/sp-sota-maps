#include <Python.h>

#include <mapnik/cairo_io.hpp>
#include <mapnik/datasource_cache.hpp>
#include <mapnik/geometry/box2d.hpp>
#include <mapnik/load_map.hpp>
#include <mapnik/map.hpp>

PyObject *render_carto(PyObject *self, PyObject *args) {
  int width;
  int height;
  char *epsg;
  double xl, yl, xh, yh;
  char *file;

  if (!PyArg_ParseTuple(args, "iisdddds", &width, &height, &epsg, &xl, &yl, &xh,
                        &yh, &file))
    return nullptr;

  mapnik::Map map(width, height);

  mapnik::load_map(map,
                   "../openstreetmap-carto/carto.xml",
                   false, "../openstreetmap-carto");
  map.set_srs(epsg);
  map.zoom_to_box(mapnik::box2d<double>(xl, yl, xh, yh));
  mapnik::save_to_cairo_file(map, file);


  Py_RETURN_NONE;
}

static PyMethodDef render_carto_methods[] = {
    {"render_carto", (PyCFunction)render_carto, METH_VARARGS,
     "Render carto map with given parameters."},
    {nullptr, nullptr, 0, nullptr}};

static struct PyModuleDef render_carto_module = {
    PyModuleDef_HEAD_INIT, "render_carto", nullptr, -1, render_carto_methods,
};

PyMODINIT_FUNC PyInit_render_carto(void) {

  mapnik::datasource_cache::instance().register_datasources(
      "/usr/lib/mapnik/input/");

  return PyModule_Create(&render_carto_module);
}
