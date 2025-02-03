from .kubernetes import k8s


def get_resource_types():
    r = k8s.get_api_resources()
    breakpoint()
    a = 1
    return r
