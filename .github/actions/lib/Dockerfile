FROM debian:trixie-slim

RUN apt -y update && apt -y install python3-pip libmapnik-dev

COPY ../../../ /sp-sota-maps

RUN pip install --break-system-packages /sp-sota-maps/lib/

ENTRYPOINT ["sh", "-c", "python -m sota.scripts.$SCRIPT $ARGS"]
