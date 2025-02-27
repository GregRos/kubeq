from typing import Any, Awaitable, Callable
import aioreactive as rx


def to_list[_T]() -> Callable[[rx.AsyncObservable[_T]], rx.AsyncObservable[list[_T]]]:
    return lambda x: rx.take_last(1)(rx.scan(lambda acc, x: acc + [x], [])(x))


def run[_T](source: rx.AsyncObservable[_T]) -> Awaitable[_T]:
    return rx.run(source, timeout=1200 * 2)
