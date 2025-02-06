from kubeq.query import *


def decide(selectors: list[Selector]):
    squashed = SelectionFormula.squash(selectors)
    finite_sets = {at: red.base_reducerattr) for attr in squashed}
    if attr.Kind() in squashed:
        return squashed[attr.Kind()]
