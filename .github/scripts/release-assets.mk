#!/usr/bin/env -S make -f

SOTA_OUTPUT ?= ./output
GITHUB_REF_NAME ?= $(shell git describe --tags `git rev-list --tags --max-count=1`)

SUMMITS = $(shell \
    cat ${SOTA_OUTPUT}/summits.csv |\
    tail -n +2 |\
    awk 'BEGIN { FS = ","; ORS = " " } NF { gsub(/[/-]/,""); print $$1 }' ;\
)

PDFS = $(SUMMITS:%=$(SOTA_OUTPUT)/%.pdf)
PNGS = $(SUMMITS:%=$(SOTA_OUTPUT)/%.png)
AVIFS = $(SUMMITS:%=$(SOTA_OUTPUT)/%.avif)
GEOJSONS = $(SUMMITS:%=$(SOTA_OUTPUT)/%.geojson)


.PHONY = upload
upload: \
    $(SOTA_OUTPUT)/summits.csv \
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

$(PDFS): %.pdf: $(SOTA_OUTPUT)/summits.csv
	test -f $@
	touch $@

$(PNGS): %.png: %.pdf
	magick convert -density 512 -resize x1440 \$< -flatten \$@
	optipng \$@

$(AVIFS): %.avif: %.png
	magick convert \$< \$@

$(GEOJSONS): %.geojson: $(SOTA_OUTPUT)/summits.csv
	test -f $@
	touch $@
