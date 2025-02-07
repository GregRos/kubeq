from dataclasses import dataclass
from mimetypes import MimeTypes
from sys import api_version
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


@dataclass
class AcceptSubclause:
    version: str
    group: str
    as_: str
    content_type: str = "application/json"

    def with_(
        self,
        *,
        as_: str | None = None,
        content_type: str | None = None,
        group: str | None = None,
        version: str | None = None,
    ):
        return AcceptSubclause(
            version=version or self.version,
            group=group or self.group,
            as_=as_ or self.as_,
            content_type=content_type or self.content_type,
        )

    def __str__(self):
        as_with_mime = f"{self.as_},{self.content_type}"
        pairs = [("g", self.group), ("v", self.version), ("as", as_with_mime)]
        return _from_sections([_format_kvp(k, v) for k, v in pairs])


class AcceptHeader:
    content_type: str
    subclauses: tuple[AcceptSubclause, ...]

    def __init__(self, content_type: str, *subclause: AcceptSubclause):
        self.content_type = content_type
        self.subclauses = subclause

    def __str__(self):
        sections = _from_sections(self.content_type, *[str(s) for s in self.subclauses])
        return sections
