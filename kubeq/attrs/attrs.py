from dataclasses import dataclass
from tkinter import Attr
from typing import (
    Any,
    ClassVar,
    Literal,
    Protocol,
    TypeGuard,
    TypeIs,
    runtime_checkable,
)

from kr8s.objects import APIObject


from kubeq.operators.operators import AnyOp, ApiOp


@dataclass
class Label:
    __match_args__ = ["key"]
    name: str

    def get(self, object: APIObject) -> str:
        return object.labels.get(self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Label) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Field:
    __match_args__ = ["key"]
    name: str

    def get(self, object: APIObject) -> str:
        return getattr(object.raw, self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Field) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Kind:
    __match_args__ = []

    @property
    def name(self) -> str:
        return "kind"

    def get(self, object: APIObject) -> str:
        return object.kind

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Kind)

    def __hash__(self) -> int:
        return hash("kind")
