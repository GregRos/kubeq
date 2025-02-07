from dataclasses import dataclass
from mimetypes import MimeTypes
from sys import api_version
from typing import Any, Iterable, overload
from ._format import _from_sections, _format_kvp

# https://github.com/kubernetes/kubectl/issues/1712


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
