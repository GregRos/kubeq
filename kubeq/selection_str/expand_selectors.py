from itertools import groupby, product
from typing import Iterable
from kubeq import attr
import kubeq.operators as oprs
from kubeq.selection.selector import Selector
from kubeq.selection_str.to_selector_str import to_selector_str


def expand_selector(selector: Selector) -> Iterable[Selector]:
    op = oprs.Or.of(selector.operator)
    for x in op.operands:
        yield Selector(selector.attr, x)


def multiplex_complex_selectors(
    sels: dict[attr.Any, Selector]
) -> Iterable[dict[attr.Any, Selector]]:
    selector_lists = [expand_selector(x) for x in sels.values()]
    for x in product(*selector_lists):
        yield {sel.attr: sel for sel in x}
