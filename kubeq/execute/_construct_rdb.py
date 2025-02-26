from typing import Unpack
from kr8s import Api

from kubeq.entities._db import KubeResourceDB
from kubeq.http._client._client import KubeClient
from kubeq.http._requests._api_resources_request import KubeDiscoveryRequest
import aioreactive as rx

from kubeq.storage._features import CacheFeatures
from kubeq.utils import rxq


def construct_rdb(client: KubeClient, **cache_features: Unpack[CacheFeatures]):
    reqs = [
        KubeDiscoveryRequest(True, **cache_features),
        KubeDiscoveryRequest(False, **cache_features),
    ]
    res = rx.pipe(
        rx.from_iterable(reqs),
        rx.flat_map(lambda r: client.send(r)),
        rxq.to_list(),
        rx.map(KubeResourceDB),
        rxq.run,
    )
    return res
