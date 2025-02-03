import aioreactive as rx
from kr8s import Api
from kr8s.objects import APIObject


class ObjectUnion:
    def __init__(self, *inputs: rx.AsyncObservable[APIObject]):
        self.inputs = inputs

    async def __call__(self, api: Api) -> rx.AsyncObservable[APIObject]:
        return rx.pipe(rx.from_iterable(self.inputs), rx.merge_inner())
