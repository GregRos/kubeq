from kubeq.query import *


def decide(selectors: list[Selector]):
    squashed = SelectionFormula.squash(selectors)
    if attr.Kind() in squashed:
        return squashed[attr.Kind()]
