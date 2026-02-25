# SP SOTA MAPS

============

![example](example.png)

The aim of the project is to prepare a set of SOTA activation cheat sheet maps containing an activation zone and other useful features, like grid square references or nearby references from other programs.

Due to the data sources used, the coverage of the project is limited to SP region and neighbours border summits.

## Python helper library

---------------------

### Installation

```sh
pip install --user --break-system-packages --verbose ./lib
```

This will install the `sota` Python module, together with the `sota` helper executable.

### Baking or preloading the cache

A file system cache is used by the library to reduce heavy, repetitive calculations and load on the data servers.
The cache directory is specified by the `SOTA_CACHE` environment variable and defaults to `./cache`.

Baking process is recommended if all or bigger amount of summits will be processed.
In case of processing only one summit, it is enough to relay on the on demand cache generation.

To run the baking, execute the following:

```sh
sota cache bake
```

Alternatively, the cache can be preloaded from the GitHub release by executing the following:

```text
sota cache preload
```

> [!CAUTION]
> Cache uses `pickle` as a storage format, which allows arbitrary code execution during unpickling.
> Ensure you trust me and the GitHub.

### Rendering map layers and other files

All map layers will be plotted and saved as PDF files. Besides that, TEX and other files will be generated.
The output directory is specified by the `SOTA_OUTPUT` environment variable and defaults to `./output`.

Additionally, OpenStreetMap Carto has to be present in `../openstreetmap-carto/` and prepared according to: <https://github.com/gravitystorm/openstreetmap-carto/blob/master/DOCKER.md>
Poland OSM data is required: <https://download.geofabrik.de/europe/poland-latest.osm.pbf>

To run the rendering process, execute the following:

```sh
sota render
```

### Typeset the result

Final typesetting have to be done with `lualatex`.
Recommended way is to do it is with `latexmk`. This ensures files are generated correctly.

The output directory is specified by the `SOTA_OUTPUT` environment variable and defaults to `./output`.

To run the final typesetting, execute the following:

```sh
latexmk -lualatex -output-directory=$SOTA_OUTPUT $SOTA_OUTPUT/*.tex
```
