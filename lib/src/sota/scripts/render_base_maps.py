from sys import exit
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich.logging import RichHandler
from subprocess import run
import logging

logging.basicConfig(handlers=[RichHandler()])

from ..summit import Summit
from ..helpers.view_port import ViewPort
from ..render_carto import render_carto


def main() -> int:

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("{task.fields[extra]}"),
    ) as progress:
        task = progress.add_task("Plotting zones", total=len(Summit), extra="")
        for summit in Summit:
            progress.update(task, extra=f"{summit.reference}")
            vp = ViewPort.new(0.210, 0.148, 0.02, summit)
            render_carto(
                int(vp.figsize[0] * 72),
                int(vp.figsize[1] * 72),
                f"epsg:{vp.epsg}",
                *vp.bbox.xyxy,
                f"./output/{summit.reference:slug}.osm.pdf",
            )
            progress.advance(task)
        progress.update(task, extra="done!")

    return 0


if __name__ == "__main__":
    exit(main())

