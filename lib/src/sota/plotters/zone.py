from . import Config, OUTPUT_DIR, init
from ..helpers.view_port import ViewPort
from ..summit import Summit

from os.path import isfile, basename, join
import cartopy.crs as ccrs


def plot_zone(config: Config, summit: Summit):

    path = join(OUTPUT_DIR, f"{summit.reference:slug}.zone.pdf")

    if isfile(path):
        return

    fig, ax = init(ViewPort.new(config.width, config.height, config.margin, summit))

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

    fig.savefig(path, transparent=True)
