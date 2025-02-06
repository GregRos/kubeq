from kubeq.attr.kind import Kind
from kubeq.selection.selection_formula import SelectionFormula
from kubeq.selection.selector import Selector
from kubeq.

def decide(selectors: list[Selector]):
    squashed = SelectionFormula.squash(selectors)
    if Kind() in squashed:
        return squashed[Kind()]
