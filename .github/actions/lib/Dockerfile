FROM debian:trixe-slim

RUN apt-get python3-pip libmapnik-dev

COPY lib/ lib/

RUN pip install ./lib/

ENTRYPOINT ["sh", "-c", "python -m sota.scripts.$SCRIPT $ARGS"]
