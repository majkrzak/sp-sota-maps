#include <Python.h>

#include <filesystem>
#include <mutex>
#include <stdlib.h>

#include <sdbus-c++/sdbus-c++.h>

#include <mapnik/cairo_io.hpp>
#include <mapnik/datasource_cache.hpp>
#include <mapnik/geometry/box2d.hpp>
#include <mapnik/load_map.hpp>
#include <mapnik/map.hpp>

std::once_flag init;

PyObject *render_carto(PyObject *self, PyObject *args) {
  int width;
  int height;
  char *epsg;
  double xl, yl, xh, yh;
  char *file;

  std::call_once(init, []() {
    mapnik::datasource_cache::instance().register_datasources(MAPNIK_PLUGINDIR);

    auto connection = sdbus::createSessionBusConnection();
    auto systemd = sdbus::createProxy(
        *connection, sdbus::ServiceName{"org.freedesktop.systemd1"},
        sdbus::ObjectPath{"/org/freedesktop/systemd1"});
    {
      auto method = systemd->createMethodCall(
          sdbus::InterfaceName{"org.freedesktop.systemd1.Manager"},
          sdbus::MethodName{"LinkUnitFiles"});
      method << std::array{CARTO_SERVICE} << true << false;
      systemd->callMethod(method);
    }
    {
      auto method = systemd->createMethodCall(
          sdbus::InterfaceName{"org.freedesktop.systemd1.Manager"},
          sdbus::MethodName{"StartUnit"});
      method << std::filesystem::path{CARTO_SERVICE}.filename() << "replace";
      systemd->callMethod(method);
    }

    setenv("PGHOST",
           (std::filesystem::path{getenv("XDG_RUNTIME_DIR")} /
            std::filesystem::path{CARTO_SERVICE}.filename())
               .c_str(),
           true);
  });

  if (!PyArg_ParseTuple(args, "iisdddds", &width, &height, &epsg, &xl, &yl, &xh,
                        &yh, &file))
    return nullptr;

  mapnik::Map map(width, height);

  mapnik::load_map(map, CARTO_DIR "/carto.xml", false, CARTO_DIR);
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
  return PyModule_Create(&render_carto_module);
}
