from kubeq.query import *


def decide(selectors: list[Selector]):
    squashed = SelectionFormula.squash(selectors)
    kind_operator = squashed[attr.Kind()]
