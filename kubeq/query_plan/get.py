from kr8s import Api
from kr8s.objects import APIObject
from kubeq.selection.Label import Label
from kubeq.selection.Field import Field
import aioreactive as rx

from kubeq.selection.selector import ApiSelector, Selector


def to_selector(selector: Selector):
    return f"{selector.attr.name}{selector.operator.symbol}{selector.operator.value}"


class ListRequest:

    def __init__(self, kind: str, selectors: list[Selector]):
        self.kind = kind
        self.label_selectors = ",".join(to_selector(x) for x in selectors if x.is_label)
        self.field_selectors = ",".join(to_selector(x) for x in selectors if x.is_field)

    async def __call__(self, api: Api):
        return rx.from_async_iterable(
            api.async_get(
                self.kind,
                label_selector=self.label_selectors,
                field_selector=self.field_selectors,
            )
        )
