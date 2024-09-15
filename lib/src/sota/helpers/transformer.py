from pyproj import CRS, Transformer


def transformer(source_epsg: int, dest_espg: int) -> Transformer:
    return Transformer.from_crs(
        CRS.from_epsg(source_epsg), CRS.from_epsg(dest_espg), always_xy=True
    )
