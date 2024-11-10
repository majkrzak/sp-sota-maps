from . import Config, OUTPUT_DIR
from ..helpers.view_port import ViewPort
from ..summit import Summit

from os.path import isfile, basename, join
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def plot_zone(config: Config, summit: Summit):

    path = join(OUTPUT_DIR, f"{summit.reference:slug}.zone.pdf")

    if isfile(path):
        return

    vp = ViewPort.new(config.width, config.height, config.margin, summit)

    fig = plt.figure(figsize=vp.figsize)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    ax = plt.axes(projection=ccrs.epsg(vp.epsg))
    ax.set_extent(vp.bbox.xxyy, crs=ccrs.epsg(vp.epsg))

    ax.add_geometries(
        summit.zone.shape,
        crs=ccrs.PlateCarree(),
        styler=lambda _: {
            "facecolor": "none",
            "edgecolor": "black",
            "antialiased": True,
            "linewidth": 1,
            "alpha": 3 / 4,
        },
    )

    plt.savefig(path, transparent=True)
    plt.close()
