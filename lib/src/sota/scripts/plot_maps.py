from sys import exit
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich.logging import RichHandler
import logging

logging.basicConfig(handlers=[RichHandler()])

from ..summit import Summit
from ..plotters import Config
from ..plotters.zone import plot_zone


def main() -> int:

    plot_config = Config(0.210, 0.148, 0.02)

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("{task.fields[extra]}"),
    ) as progress:
        task = progress.add_task("Ploting zones", total=len(Summit), extra="")
        for summit in Summit:
            progress.update(task, extra=f"{summit.reference}")
            plot_zone(plot_config, summit)
            progress.advance(task)
        progress.update(task, extra="done!")
    return 0


if __name__ == "__main__":
    exit(main())
