import types
from kr8s import api, Api


def kr8s_api():
    original_construct_url = getattr(Api, "_construct_url")

    def my_construct_url(
        self,
        version: str = "v1",
        base: str = "",
        namespace: str | None = None,
        url: str = "",
    ):
        if not version and not base and not namespace:
            return url
        return original_construct_url(self, version, base, namespace, url)

    a = api()
    setattr(a, "_construct_url", types.MethodType(my_construct_url, a))
    return a
