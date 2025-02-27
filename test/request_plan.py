import asyncio
import logging
from kr8s import api
from kubeq.execute._exec_query import QueryExecution
from kubeq.http._client._client import KubeClient
from kubeq.logging._setup_logging import setup_logging
from kubeq.query._attr.field import Field
from kubeq.query._attr.kind import Kind
from kubeq.query._utils.render_op import render_operator
from kubeq.query._operators import *
from kubeq.query import *
from kubeq.selection._selection_formula import SelectionFormula

setup_logging(minLevel=logging.DEBUG)


async def start():
    client = KubeClient(api(context="minikube"))
    formula = SelectionFormula(
        {
            Kind("version"): Eq("v1"),
            Kind("ident"): Glob("P*"),
            Field("metadata.namespace"): In("default", "kube-system"),
        }+
    )
    exec = QueryExecution(client, formula)
    results = await exec.run()
    for r in results:
        print(f"- {r.metadata.name}")


asyncio.run(start())
