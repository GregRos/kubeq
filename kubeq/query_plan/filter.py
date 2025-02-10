from aioreactive import AsyncObservable, filter_async, pipe, filter
from kr8s.objects import APIObject
from kubeq.query import *
from kubeq.query._selection._instance_selector import InstanceSelector


class ObjectFilter:
    input: AsyncObservable[APIObject]

    def __init__(
        self, input: AsyncObservable[APIObject], selectors: list[InstanceSelector]
    ):
        self.input = input
        self.selectors = selectors

    def filter(self, object: APIObject) -> bool:
        return all(selector(object) for selector in self.selectors)

    async def __call__(self) -> AsyncObservable[APIObject]:
        return pipe(self.input, filter(self.filter))
