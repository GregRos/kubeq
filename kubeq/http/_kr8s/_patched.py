import types
from kr8s import api, Api
import kubernetes

# see [notes about this file](./client.md)


def kr8s_api():
    original_construct_url = getattr(Api, "_construct_url")

    def my_construct_url(
        self,
        version: str = "v1",
        base: str = "",
        namespace: str | None = None,
        url: str = "",
    ):
        # sometimes we want to force the kr8s client to send an API request to a URL verbatim
        # it can't actually do that by default, but here's a hack for doing so.
        if not version and not base and not namespace:
            # this would normally throw an exception
            return url
        return original_construct_url(self, version, base, namespace, url)

    a = api()
    setattr(a, "_construct_url", types.MethodType(my_construct_url, a))
    return a
