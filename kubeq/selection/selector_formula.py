from ast import Or
from kubeq.selection.selector import Attr, Selector


class SelectionAnd:
    def __init__(self, selectors: dict[Attr, Or]):
        self.selectors = selectors
