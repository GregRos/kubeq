from typing import Any, Callable
import aioreactive as rx


def to_list[_T]() -> Callable[[rx.AsyncObservable[_T]], rx.AsyncObservable[list[_T]]]:
    return rx.reduce(lambda acc, x: acc + [x], [])
