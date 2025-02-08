from asyncio import gather
import asyncio
from datetime import datetime
from kr8s import api

import yaml


def start():
    k = kr8s_api()

    async def send(url: str):
        result = k.call_api(
            method="GET",
            base="",
            version="",
            raise_for_status=True,
            namespace=None,
            url=url,
            headers={
                "User-Agent": "kubeq/0.0.0 (linux; amd64)",
                "X-Cache-Control": "1",
                "Accept": str(_accept_for_discovery),
            },
            data=None,
        )
        async with result as response:
            return response.json()

    async def all_payloads():
        api_result = send("/api")
        apis_result = send("/apis")
        r1, r2 = await gather(api_result, apis_result)
        # write to a file `result.{RANDOM}.yaml`
        timestamp = datetime.now().time().strftime("%H_%M_%S")
        with open(f"result.{timestamp}.yaml", "w") as f:
            yaml.dump_all([r1, r2], f)

    asyncio.run(all_payloads())
