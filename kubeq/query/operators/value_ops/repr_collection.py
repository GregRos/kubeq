from typing import Iterable


def repr_collection(xs: Iterable[str]) -> str:
    stuff = ", ".join([f"{v!r}" for v in xs])
    return stuff
