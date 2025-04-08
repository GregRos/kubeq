from dataclasses import dataclass
from mimetypes import MimeTypes
from sys import api_version
from typing import Any, Iterable, overload
from ._format import _from_sections, _format_kvp

# https://github.com/kubernetes/kubectl/issues/1712


@dataclass
class ComplexSubclause:
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
        return ComplexSubclause(
            version=version or self.version,
            group=group or self.group,
            as_=as_ or self.as_,
            content_type=content_type or self.content_type,
        )

    def __str__(self):
        pairs = [("g", self.group), ("v", self.version), ("as", self.as_)]
        kvps = [_format_kvp(k, v) for k, v in pairs]
        return _from_sections([self.content_type, *kvps])


class BasicSubclause:
    content_type: str

    def __init__(self, content_type: str):
        self.content_type = content_type

    def __str__(self):
        return self.content_type


type Subclause = ComplexSubclause | BasicSubclause


class AcceptHeader:
    subclauses: tuple[Subclause, ...]

    def __init__(self, *subclauses: Subclause):
        self.subclauses = subclauses

    def __str__(self):
        sections = ",".join([str(s) for s in self.subclauses])
        return sections
