import asyncio
import logging
from kr8s import api
from kubeq.execute._exec_query import KubeQ
from kubeq.http._client._client import KubeClient
from kubeq.logging._setup_logging import setup_logging
from kubeq.query._attr.field import Field
from kubeq.query._attr.kind import Kind
from kubeq.query._utils.render_op import render_operator
from kubeq.query._operators import *
from kubeq.query import *
from kubeq.selection._selection_formula import SelectionFormula

setup_logging(minLevel=logging.DEBUG)
import aioreactive as rx


async def start():
    client = KubeClient(api(context="minikube"))
    formula = SelectionFormula(
        {
            Kind("version"): Eq("v1") | Eq("v2"),
            Kind("ident"): Glob("P*"),
            Field("metadata.namespace"): In("default", "kube-system"),
        }
    )
    exec = KubeQ(client)
    results = await exec.query(formula)
    for r in results:
        print(f"- {r.metadata.name}")


asyncio.run(start())
