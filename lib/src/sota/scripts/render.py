from sys import exit
from click import command, option
from rich_click import RichCommand
from ..layers import LAYERS
from ..summit import Summit
from concurrent.futures import ThreadPoolExecutor
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich.logging import RichHandler
from ..view_port import ViewPort
import logging


@command(cls=RichCommand)
@option("-r", "--overwrite", type=bool, default=False)
def main(overwrite: bool) -> int:

    logging.basicConfig(handlers=[RichHandler()])

    executor = ThreadPoolExecutor(max_workers=5)

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
    ) as progress:
        tasks = {
            Layer.name: progress.add_task(
                f"Rendering {Layer.name} layer", total=len(Summit)
            )
            for Layer in LAYERS
        }

        for summit in Summit:

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
