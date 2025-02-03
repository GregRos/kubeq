from dataclasses import dataclass
from tkinter import Entry
from typing import Any, ClassVar, Literal, Protocol, runtime_checkable

from cdk8s

from operators.definitions import AnyOp, ApiOp, Op

type EntryType = Literal["field", "label", "namespace", "kind"]


@dataclass
class Label:
    __match_args__ = ["key"]
    key: str
    def get(self, object: ApiObject) -> str:
        return object.metadata.labels.get(self.key, "")


@dataclass
class Field:
    __match_args__ = ["key"]
    key: str


@dataclass
class Kind:
    __match_args__ = []
    pass


type ApiEntry = Label | Field

type Entry = Label | Field | Kind


@dataclass
class Selector[E: Entry, O: Op[Any]]:
    entry: E
    op: O
    def __call__(self, )


type ApiSelector = Selector[ApiEntry, ApiOp]
