from concurrent.futures import ThreadPoolExecutor
from logging import DEBUG, ERROR, INFO, basicConfig
from os import environ
from subprocess import run
from xml.etree import ElementTree as ET

from click import group, option
from rich.logging import RichHandler
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
from rich_click import RichCommand, RichGroup

from .layers import LAYERS
from .reference import Reference
from .summit import Summit
from .view_port import ViewPort

progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    TextColumn("{task.fields[extra]}"),
)


@group(cls=RichGroup)
@option("--verbose", default=False, is_flag=True)
@option("--quiet", default=False, is_flag=True)
def main(*,verbose: bool, quiet: bool) -> None:
    basicConfig(
        level=DEBUG if verbose else ERROR if quiet else INFO, handlers=[RichHandler()],
    )


@main.group(cls=RichGroup)
def cache() -> None:
    """Cache management."""


@cache.command(cls=RichCommand)
def bake() -> None:
    """Bake the cache."""
    with progress:
        task = progress.add_task("Baking the cache", total=len(Summit), extra="")
        for summit in Summit:
            progress.update(task, extra=f"{summit.reference}")
            _ = summit.zone
            _ = summit.peak
            _ = summit.gminas
            _ = summit.parks
            _ = summit.chunk
            progress.advance(task)
        progress.update(task, extra="done!")


@cache.command(cls=RichCommand)
def preload() -> None:
    """Preload the cache."""
    raise NotImplementedError


@main.group(cls=RichGroup)
def carto() -> None:
    """Carto management."""

@carto.command(cls=RichCommand)
def load() -> None:
    """Load OSM data into the database."""
    nodes = sorted({
        node for summit in Summit for node in summit.chunk.nodes
    })
    ways = sorted({
        way for summit in Summit for way in summit.chunk.ways
    })
    relations = sorted({
        relation for summit in Summit for relation in summit.chunk.relations
    })


    root = ET.Element("osm", version="0.6")
    root.extend(n.to_xml() for n in nodes)
    root.extend(w.to_xml() for w in ways)
    root.extend(r.to_xml() for r in relations)

    run(
        [environ.get("CARTO_INIT")],
        check=False, input=ET.tostring(root),
    )

@main.command(cls=RichCommand)
@option("-r", "--overwrite", type=bool, default=False, is_flag=True)
@option("-s", "--reference", type=str)
@option("-l", "--layer", type=str)
@option("-w", "--workers", type=int, default=10)
def render(
    *,overwrite: bool, reference: str | None, layer: str | None, workers: int,
)-> None:
    """Render output."""
    executor = ThreadPoolExecutor(max_workers=workers)

    summits = Summit if not reference else [Summit[Reference.from_str(reference)]]
    layers = LAYERS if not layer else list(filter(lambda x: x.name == layer, LAYERS))

    with progress:
        tasks = {
            Layer.name: progress.add_task(
                f"Rendering {Layer.name} layer", total=len(summits), extra="",
            )
            for Layer in layers
        }

        for summit in summits:
            view_port = ViewPort.a5paper(summit)

            for Layer in layers:

                def task(layer: Layer) -> None:
                    if overwrite or not layer.exists:
                        layer.render()
                    progress.advance(tasks[layer.name])

                executor.submit(task, Layer(summit, view_port))

        executor.shutdown()


if __name__ == "__main__":
    main()
