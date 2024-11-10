from . import Config, OUTPUT_DIR
from ..helpers.view_port import ViewPort
from ..summit import Summit

from os.path import isfile, basename, join
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from math import floor, ceil


def plot_isolines(config: Config, summit: Summit):

    path = join(OUTPUT_DIR, f"{summit.reference:slug}.isolines.pdf")

    if isfile(path):
        return

    vp = ViewPort.new(config.width, config.height, config.margin, summit)

    fig = plt.figure(figsize=vp.figsize)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    ax = plt.axes(projection=ccrs.epsg(vp.epsg))
    ax.set_extent(vp.bbox.xxyy, crs=ccrs.epsg(vp.epsg))

    hmap = summit.zone.hmap

    ax.contour(
        hmap.data,
        extent=(
            hmap.bounds.xyxy[0],
            hmap.bounds.xyxy[2],
            hmap.bounds.xyxy[3],
            hmap.bounds.xyxy[1],
        ),
        transform=ccrs.epsg(hmap.bounds.epsg),
        levels=[
            i * 10
            for i in range(floor(hmap.data.min() / 10), ceil(hmap.data.max() / 10))
        ],
        linewidths=[
            0.1 if i % 10 else 0.2
            for i in range(floor(hmap.data.min() / 10), ceil(hmap.data.max() / 10))
        ],
        colors="gray",
        alpha=0.5,
    )

    plt.savefig(path, transparent=True)
    plt.close()
