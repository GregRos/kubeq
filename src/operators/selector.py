from dataclasses import dataclass
from typing import ClassVar, Literal, Protocol
from dictum.selection.operators.definitions import AnyOp

type EntryType = Literal["field", "label", "namespace", "kind"]


class Entry(Protocol):
    entry_type: ClassVar[EntryType]


@dataclass
class Label(Entry):
    entry_type: ClassVar[EntryType] = "label"
    __match_args__ = ["key"]
    key: str


@dataclass
class Field(Entry, entry_type="field"):
    __match_args__ = ["key"]
    key: str


@dataclass
class Kind(Entry, entry_type="kind"):
    __match_args__ = []
    pass


@dataclass
class Selector:
    entry: Entry
    op: AnyOp
