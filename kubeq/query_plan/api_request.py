from operators.definitions import ApiOp
from operators.selector import ApiSelector, Field, Label, Selector
import reactivex as rx


class ListRequest:

    def __init__(self, kind: str, selectors: list[ApiSelector]):
        self.kind = kind

    def __call__(self):
        
