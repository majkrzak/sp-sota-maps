from logging import basicConfig, DEBUG, ERROR, INFO
from click import group, option
from concurrent.futures import ThreadPoolExecutor
from rich.logging import RichHandler
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich_click import RichCommand, RichGroup
from typing import Optional
from .summit import Summit
from .reference import Reference
from .layers import LAYERS
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
def main(verbose: bool, quiet: bool):
    basicConfig(
        level=DEBUG if verbose else ERROR if quiet else INFO, handlers=[RichHandler()]
    )


@main.group(cls=RichGroup)
def cache():
    """Cache management"""
    pass


@cache.command(cls=RichCommand)
def bake():
    """Bake the cache"""

    with progress:
        task = progress.add_task("Baking the cache", total=len(Summit), extra="")
        for summit in Summit:
            progress.update(task, extra=f"{summit.reference}")
            _ = summit.zone
            _ = summit.peak
            _ = summit.gminas
            _ = summit.parks
            progress.advance(task)
        progress.update(task, extra="done!")
    return 0


@cache.command(cls=RichCommand)
def preload():
    """Preload the cache"""
    raise NotImplementedError()


@main.command(cls=RichCommand)
@option("-r", "--overwrite", type=bool, default=False, is_flag=True)
@option("-s", "--reference", type=str)
@option("-l", "--layer", type=str)
@option("-w", "--workers", type=int, default=10)
def render(
    overwrite: bool, reference: Optional[str], layer: Optional[str], workers: int
):
    """Render output"""
    executor = ThreadPoolExecutor(max_workers=workers)

    summits = Summit if not reference else [Summit[Reference.from_str(reference)]]
    layers = LAYERS if not layer else list(filter(lambda x: x.name == layer, LAYERS))

    with progress:
        tasks = {
            Layer.name: progress.add_task(
                f"Rendering {Layer.name} layer", total=len(summits), extra=""
            )
            for Layer in layers
        }

        for summit in summits:
            view_port = ViewPort.a5paper(summit)

            for Layer in layers:

                def task(layer):
                    if overwrite or not layer.exists:
                        layer.render()
                    progress.advance(tasks[layer.name])

                executor.submit(task, Layer(summit, view_port))

        executor.shutdown()


if __name__ == "__main__":
    main()
