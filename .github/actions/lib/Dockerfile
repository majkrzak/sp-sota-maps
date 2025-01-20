FROM debian:trixie-slim

RUN apt-get python3-pip libmapnik-dev

COPY ../../../ .

RUN pip install ./lib/

ENTRYPOINT ["sh", "-c", "python -m sota.scripts.$SCRIPT $ARGS"]
