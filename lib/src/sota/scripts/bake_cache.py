from sys import exit
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich.logging import RichHandler
import logging

logging.basicConfig(handlers=[RichHandler()])

from ..summit import Summit


def main() -> int:
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("{task.fields[extra]}"),
    ) as progress:
        task = progress.add_task("Baking the cache", total=len(Summit), extra="")
        for summit in Summit:
            progress.update(task, extra=f"{summit.reference}")
            _ = summit.zone
            _ = summit.peak
            progress.advance(task)
        progress.update(task, extra="done!")
    return 0


if __name__ == "__main__":
    exit(main())
