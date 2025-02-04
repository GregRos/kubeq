from kr8s import Api
import aioreactive as rx


class FixedResourceQuery:
    def __init__(self, api: Api, resource: str):
        self.api = api
        self.resource = resource

    async def __call__(self) -> rx.AsyncObservable:
        return self.api.get(self.resource)
