from . import Config, OUTPUT_DIR, init
from ..helpers.view_port import ViewPort
from ..summit import Summit

from os.path import isfile, basename, join
from math import floor, ceil
import cartopy.crs as ccrs
from numpy.ma import masked_array


def plot_isolines(config: Config, summit: Summit):

    path = join(OUTPUT_DIR, f"{summit.reference:slug}.isolines.pdf")

    if isfile(path):
        return

    fig, ax = init(ViewPort.new(config.width, config.height, config.margin, summit))

    hmap = summit.zone.hmap
    data = masked_array(hmap.data, mask=~(0 < hmap.data))

    ax.contour(
        data,
        extent=(
            hmap.bounds.xyxy[0],
            hmap.bounds.xyxy[2],
            hmap.bounds.xyxy[3],
            hmap.bounds.xyxy[1],
        ),
        transform=ccrs.epsg(hmap.bounds.epsg),
        levels=[i * 10 for i in range(floor(data.min() / 10), ceil(data.max() / 10))],
        linewidths=[
            0.1 if i % 10 else 0.2
            for i in range(floor(data.min() / 10), ceil(data.max() / 10))
        ],
        colors="gray",
        alpha=0.5,
    )

    fig.savefig(path, transparent=True)
