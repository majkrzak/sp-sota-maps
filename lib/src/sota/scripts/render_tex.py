from sys import exit
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from jinja2 import Environment, PackageLoader
from rich.logging import RichHandler
from datetime import datetime
import logging

logging.basicConfig(handlers=[RichHandler()])

from ..summit import Summit
from ..view_port import ViewPort
from .. import __version__


def main() -> int:

    env = Environment(
        variable_start_string="<",
        variable_end_string=">",
        loader=PackageLoader("sota", "templates"),
    )
    env.filters["slug"] = lambda value: f"{value:slug}"
    env.filters["full"] = lambda value: f"{value:full}"

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("{task.fields[extra]}"),
    ) as progress:
        task = progress.add_task("TeX-ing", total=len(Summit), extra="")
        for summit in Summit:
            progress.update(task, extra=f"{summit.reference}")
            vp = ViewPort.a5paper(summit)

            tpl = env.get_template("map.tex")
            with open(f"./output/{summit.reference:slug}.tex", "w") as f:
                f.write(
                    tpl.render(
                        slug=f"{summit.reference:slug}",
                        summit=summit,
                        view_port=vp,
                        layers=["osm", "isolines", "zone"],
                        version=__version__,
                        date=datetime.today().strftime("%Y-%m-%d"),
                    )
                )

            progress.advance(task)
        progress.update(task, extra="done!")

    return 0


if __name__ == "__main__":
    exit(main())
