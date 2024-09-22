SP SOTA MAPS
============

Aim of the project is to prepare a set of SOTA activation cheatsheet maps congaing the activation zone and other useful
features, like grid square reference or nearby references from other programs.

Due to the data sources used, the coverage of the project is limited to SP region and neighbours border summits.


Python helper library
---------------------

### Installation

```sh
pip install --user --break-system-packages --verbose ./lib
```

### Baking the cache

Filesystem cache is used by the library to reduce heavy repetitive calculations and load on the data servers.
Cache directory is specified by the `SOTA_CACHE` environment variable and defaults to `./CACHE`.

Baking process is recommended if all or bigger amount of summits will be processed.
In case of processing only one summit, it is enough to relay on the on demand cache generation.

To run the baking, execute the following:

```sh
python -m sota.scripts.bake_cache
```
