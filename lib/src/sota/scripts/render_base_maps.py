from sys import exit
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich.logging import RichHandler
from subprocess import run
import logging

logging.basicConfig(handlers=[RichHandler()])

from ..summit import Summit
from ..helpers.view_port import ViewPort


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

            res = run(
                [
                    "./lib/map_build/map_builder",
                    f"{vp.figsize[0]*72}",
                    f"{vp.figsize[1]*72}",
                    f"epsg:{vp.epsg}",
                    *map(str, vp.bbox.xyxy),
                    f"./output/{summit.reference:slug}.osm.pdf",
                ]
            )

            logging.info("", res)

            progress.advance(task)
        progress.update(task, extra="done!")

    return 0


if __name__ == "__main__":
    exit(main())


# Build osm map
for index, summit in SUMMITS[
    SUMMITS.ActivationZone.apply(lambda x: not x.is_empty)
].iterrows():
    if isfile(f"out/{summit.Slug}.osm.pdf"):
        continue

    scale = pick_scale(summit.ActivationZone, RADIUS, SCALES)
    epsg = pick_epsg(summit.Longitude, scale)
    bbox = scaled_bobx_epsg(summit.ActivationZone, *SIZE, scale, epsg)

    width = int(SIZE[0] * 72 * M2I)
    height = int(SIZE[1] * 72 * M2I)
