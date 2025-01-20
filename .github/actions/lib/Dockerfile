FROM debian:trixie-slim

RUN apt -y update && apt -y install python-is-python3 python3-pip libmapnik-dev git

RUN pip install --break-system-packages "git+https://github.com/majkrzak/sp-sota-maps.git#subdirectory=lib"

ENTRYPOINT ["sh", "-c", "python -m sota.scripts.$SCRIPT $ARGS"]
