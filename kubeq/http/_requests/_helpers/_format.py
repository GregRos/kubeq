from typing import Any, Iterable, overload


@overload
def _from_sections(*sections: str) -> str: ...
@overload
def _from_sections(sections: Iterable[str], /) -> str: ...
def _from_sections(*sections: Any) -> str:
    def _do_it(sections: Iterable[str]) -> str:
        return ";".join(sections)

    match sections:
        case (str(s), *rest):
            return _do_it(sections)
        case (sections,):
            return _do_it(sections)
        case _:
            raise ValueError("Invalid input")


def _format_kvp(k: str, v: str):
    return f"{k}={v}"
