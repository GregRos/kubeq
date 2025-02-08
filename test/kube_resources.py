from asyncio import gather
import asyncio
from datetime import datetime
from typing import Any
from kr8s import api
from kubeq.http import KubeClient, KubeDiscoveryRequest, KubeRequest, KubeRxRequest
import yaml
import aioreactive as rx


def start():
    async def do():

        client = KubeClient(api())
        pair = client.send(KubeDiscoveryRequest(True)), client.send(
            KubeDiscoveryRequest(False)
        )

        res = rx.pipe(res, rx.map(print))
        await rx.run(res)

    asyncio.run(do())
