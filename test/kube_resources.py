from asyncio import gather
import asyncio
from datetime import datetime
import logging
from typing import Any
from kr8s import api
from kubeq.http import KubeClient, KubeDiscoveryRequest, KubeRequest, KubeRxRequest
import yaml
import aioreactive as rx

from kubeq.logging import setup_logging
from kubeq.utils import rxq

setup_logging(minLevel=logging.DEBUG)
import aioreactive


def start():
    async def do():

        client = KubeClient(api())
        reqs = [
            KubeDiscoveryRequest(True, cache_ttl=50, cache_force=True),
            KubeDiscoveryRequest(False, cache_ttl=50, cache_force=True),
        ]

        res = await rx.pipe(
            rx.from_iterable(reqs),
            rx.merge(rx.from_iterable(reqs)),
            rx.flat_map(lambda r: client.send(r)),
            rxq.to_list(),
            rxq.run,
        )

    asyncio.run(do())
