from typing import Any, Callable, Type


def dunder_invoker(dunder_name: str) -> Callable[[object], Any]:
    name = f"{dunder_name}"

    def _get_dunder(obj):
        if not hasattr(obj, name):
            raise ValueError(f"Object {obj} does not have {name}")
        if not callable(getattr(obj, name)):
            raise ValueError(f"Object {obj} has a non-callable {name}")
        v = getattr(obj, name)()

        return v

    return _get_dunder
