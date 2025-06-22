#!/usr/bin/env -S make -f

SOTA_CACHE ?= ./cache
SOTA_OUTPUT ?= ./output
GITHUB_REF_NAME ?= $(shell git describe --tags `git rev-list --tags --max-count=1`)

SUMMITS = $(shell .github/scripts/list-slugs.py)

PDFS = $(SUMMITS:%=$(SOTA_OUTPUT)/%.pdf)
PNGS = $(SUMMITS:%=$(SOTA_OUTPUT)/%.png)
AVIFS = $(SUMMITS:%=$(SOTA_OUTPUT)/%.avif)
GEOJSONS = $(SUMMITS:%=$(SOTA_OUTPUT)/%.geojson)


.PHONY = upload
upload: \
    $(SOTA_OUTPUT)/pdf.tar \
    $(SOTA_OUTPUT)/png.tar \
    $(SOTA_OUTPUT)/avif.tar \
    $(SOTA_OUTPUT)/geojson.tar \
    $(PDFS) $(PNGS) $(AVIFS) $(GEOJSONS)
	for f in $^; do gh release upload $(GITHUB_REF_NAME) $$f || true; done

%.tar:
	tar --create --owner 0 --group 0 --transform='s,.*/,,' --mode='a=r' --file $@ $^

$(SOTA_OUTPUT)/pdf.tar: $(PDFS)
$(SOTA_OUTPUT)/png.tar: $(PNGS)
$(SOTA_OUTPUT)/avif.tar: $(AVIFS)
$(SOTA_OUTPUT)/geojson.tar: $(GEOJSONS)

$(PDFS): %.pdf: %.tex %.zone.pdf %.isolines.pdf %.osm.pdf
	latexmk -lualatex -output-directory=$(SOTA_OUTPUT) $<

$(PNGS): %.png: %.pdf
	magick convert -density 512 -resize x1440 \$< -flatten \$@
	optipng \$@

$(AVIFS): %.avif: %.png
	magick convert \$< \$@

$(GEOJSONS): %.geojson:
	test -f $@
	touch $@
