import inspect
from typing import Callable


def get_class_methods(cls) -> dict[str, Callable]:
    return {
        name: f
        for name, f in cls.__dict__.items()
        if inspect.isfunction(f) or inspect.ismethod(f)
    }
