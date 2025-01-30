from sys import exit
from click import command, option
from rich_click import RichCommand
from typing import Optional
from concurrent.futures import ThreadPoolExecutor
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich.logging import RichHandler
import logging

logging.basicConfig(handlers=[RichHandler()])

from ..layers import LAYERS
from ..summit import Summit
from ..reference import Reference
from ..view_port import ViewPort


@command(cls=RichCommand)
@option("-r", "--overwrite", type=bool, default=False)
@option("-s", "--reference", type=str)
def main(overwrite: bool, reference: Optional[str]) -> int:
    executor = ThreadPoolExecutor(max_workers=1)

    summits = Summit if not reference else [Summit[Reference.from_str(reference)]]

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
    ) as progress:
        tasks = {
            Layer.name: progress.add_task(
                f"Rendering {Layer.name} layer", total=len(summits)
            )
            for Layer in LAYERS
        }

        for summit in summits:

            view_port = ViewPort.a5paper(summit)

            for Layer in LAYERS:

                def task(layer):
                    if overwrite or not layer.exists:
                        layer.render()
                    progress.advance(tasks[layer.name])

                executor.submit(task, Layer(summit, view_port))

        executor.shutdown()


if __name__ == "__main__":
    exit(main())
