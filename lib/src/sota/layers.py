from abc import ABC, abstractmethod
from dataclasses import dataclass
from os import environ
from .summit import Summit
from .view_port import ViewPort
from matplotlib.pyplot import Figure, Axes
import cartopy.crs as ccrs
from .render_carto import render_carto
from os.path import join, isfile
from numpy.ma import masked_array
from math import floor, ceil

OUTPUT_DIR = environ.get("SOTA_OUTPUT", "./output")


@dataclass
class Layer(ABC):
    summit: Summit
    view_port: ViewPort

    @abstractmethod
    def render(self) -> None:
        pass

    @property
    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @property
    def path(self) -> str:
        return join(OUTPUT_DIR, f"{self.summit.reference:slug}.{self.name}.pdf")

    @property
    def exists(self) -> bool:
        return isfile(self.path)


@dataclass
class PyplotLayer(Layer):

    def render(self) -> None:
        fig = Figure(figsize=self.view_port.figsize)
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

        ax = fig.add_subplot(projection=ccrs.epsg(self.view_port.epsg))
        ax.set_extent(self.view_port.bbox.xxyy, crs=ccrs.epsg(self.view_port.epsg))

        self.plot(ax)

        fig.savefig(self.path, transparent=True)

    @abstractmethod
    def plot(self, fig: Figure, ax: Axes) -> None:
        pass


@dataclass
class ZoneLayer(PyplotLayer):
    name = "zone"

    def plot(self, ax) -> None:
        ax.add_geometries(
            self.summit.zone.shape,
            crs=ccrs.PlateCarree(),
            styler=lambda _: {
                "facecolor": "none",
                "edgecolor": "black",
                "antialiased": True,
                "linewidth": 1,
                "alpha": 3 / 4,
            },
        )


@dataclass
class IsolinesLayer(PyplotLayer):
    name = "isolines"

    def plot(self, ax) -> None:
        hmap = self.summit.zone.hmap
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
            levels=[
                i * 10 for i in range(floor(data.min() / 10), ceil(data.max() / 10))
            ],
            linewidths=[
                0.1 if i % 10 else 0.2
                for i in range(floor(data.min() / 10), ceil(data.max() / 10))
            ],
            colors="gray",
            alpha=0.5,
        )


@dataclass
class CartoLayer(Layer):
    name = "osm"

    def render(self) -> None:
        render_carto(
            int(self.view_port.figsize[0] * 72),
            int(self.view_port.figsize[1] * 72),
            f"epsg:{self.view_port.epsg}",
            *self.view_port.bbox.xyxy,
            self.path,
        )


LAYERS = (CartoLayer, IsolinesLayer, ZoneLayer)
