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
from kubeq.query._attr.kind import Kind
from kubeq.query_plan.decide import QueryDecider
from kubeq.utils import rxq
import pprint

from rich.console import Console

from kubeq.viz._rdb._table import Table_RDB

setup_logging(minLevel=logging.DEBUG)
import aioreactive

c = Console()


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
        table = Table_RDB(resources)
        c.print(table)
        qd = QueryDecider(resources, client)
        select_pods = Kind("name").eq("Pod")
        rx_results = qd.query(select_pods)

        res2 = await rx.pipe(
            rx_results,
            rxq.to_list(),
            rxq.run,
        )
        c.print(res2)

    asyncio.run(do())
