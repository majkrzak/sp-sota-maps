from .summit import Summit

def slugs():
    print(*(f"{summit.reference:slug}" for summit in Summit), sep=" ", end="")

QUERIES = (slugs,)
