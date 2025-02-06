from typing import Any, Iterable


def collection_repr(name: str, sep: str, collection: Iterable[Any]) -> str:
    stuff = sep.join([f"{v!r}" for v in collection])
    return f"{name}({stuff})"
