from asyncio import gather
import asyncio
from datetime import datetime
import logging
from typing import Any
from kr8s import api
from kubeq.http import KubeClient, KubeDiscoveryRequest, KubeRequest, KubeRxRequest
from kubeq.entities import KubeKind, KubeResourceDB
import yaml
import aioreactive as rx

from kubeq.logging import setup_logging
from kubeq.utils import rxq
import pprint

from kubeq.viz._print_rdb import print_rdb

setup_logging(minLevel=logging.DEBUG)
import aioreactive


def start():
    async def do():

        client = KubeClient(api())
        reqs = [
            KubeDiscoveryRequest(True, cache_ttl=50),
            KubeDiscoveryRequest(False, cache_ttl=50),
        ]

        res = await rx.pipe(
            rx.from_iterable(reqs),
            rx.flat_map(lambda r: client.send(r)),
            rxq.to_list(),
            rxq.run,
        )

        resources = KubeResourceDB(res)
        print_rdb(resources)

    asyncio.run(do())
