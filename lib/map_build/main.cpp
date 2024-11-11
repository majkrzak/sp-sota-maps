#include <string>
#include <mapnik/map.hpp>
#include <mapnik/load_map.hpp>
#include <mapnik/datasource_cache.hpp>
#include <mapnik/geometry/box2d.hpp>
#include <mapnik/cairo_io.hpp>

int main(int argc, char * argv[]) {

    int width = std::stoi(argv[1]);
    int height = std::stoi(argv[2]);
    char* epsg = argv[3];
    double xl = std::stoi(argv[4]);
    double yl = std::stoi(argv[5]);
    double xh = std::stoi(argv[6]);
    double yh = std::stoi(argv[7]);
    char* file = argv[8];

    mapnik::datasource_cache::instance().register_datasources("/usr/lib/mapnik/input/");
    mapnik::Map map(width,height);
    mapnik::load_map(map, "./openstreetmap-carto/carto.xml", false, "./openstreetmap-carto");
    map.set_srs(epsg);

    map.zoom_to_box(mapnik::box2d<double>(xl, yl, xh, yh));


    mapnik::save_to_cairo_file(map, file);

    return 0;
}