from dictum.init.kubernetes import K, k8s
from kr8s import objects, api


async def find_all_resources():
    k8s2 = api()
    names = await k8s2.async_api_resources()
    breakpoint()
    x = 1
    return names
