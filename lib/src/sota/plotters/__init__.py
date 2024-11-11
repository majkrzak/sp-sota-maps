from dataclasses import dataclass
from os import environ
from matplotlib.pyplot import Figure, Axes, axes
import cartopy.crs as ccrs
from ..helpers.view_port import ViewPort

OUTPUT_DIR = environ.get("SOTA_OUTPUT", "./output")


def init(view_port: ViewPort) -> (Figure, Axes):

    fig = Figure(figsize=view_port.figsize)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    ax = fig.add_subplot(projection=ccrs.epsg(view_port.epsg))
    ax.set_extent(view_port.bbox.xxyy, crs=ccrs.epsg(view_port.epsg))

    return fig, ax


@dataclass
class Config:
    width: float
    height: float
    margin: float
