from dataclasses import dataclass
from typing import Literal

from dictum.selection.selectors.operators.definitions import (
    AnyOperator,
    OperatorType,
    get_operator_type,
)

type Subject = Literal["field", "label", "kind", "namespace"]


@dataclass
class Selector:
    key: str
    subject: Subject
    op: AnyOperator
    value: str

    @property
    def operator_type(self) -> OperatorType:
        return get_operator_type(self.op)

    @property
    def is_api_supported(self) -> bool:
        return self.operator_type == "api" and self.subject in ["field", "label"]
