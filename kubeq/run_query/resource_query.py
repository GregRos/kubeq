from itertools import product
from typing import Iterable, Sequence
from kr8s import Api
import kr8s

from kubeq.entities._resource._resource import KubeResource
from kubeq.http._requests._helpers._kube_selector import splat
from kubeq.logging import sources
from kubeq.query._selection._selection_formula import SelectionFormula
import kubeq.query._attr as attr
from kubeq.query_plan.op_to_str import _selector_to_kube_api, formula_to_kube_api
from kubeq.run_query.separate import separate_formula
from ._kube_reductions import To_Min_Kube_Api_Supported
import aioreactive as rx

logger = sources.driver.logger


class RemoteQueryDriver:
    def __init__(self, api: Api):
        self._api = api

    def _make_request(self, resource: KubeResource, formula: SelectionFormula):
        labels = formula.only_of(attr.Label)
        fields = formula.only_of(attr.Field)
        labels_q = formula_to_kube_api(labels)
        fields_q = formula_to_kube_api(fields)
        labels_str = splat(labels_q)
        fields_str = splat(fields_q)
        logger.info(
            f"Querying {resource.kind.fqn} with labels {labels_str} and fields {fields_str}"
        )
        x = self._api.async_get(
            kind=resource.kind.fqn,
            labels=labels_str,
            fields=fields_str,
            namespace=kr8s.ALL,
        )
        return rx.from_async_iterable(x)

    def run(
        self, resources: Sequence[KubeResource], selection_formula: SelectionFormula
    ):
        def _run_on_resource_subquery(pair: tuple[KubeResource, SelectionFormula]):
            resource, subquery = pair
            return self._make_request(resource, subquery)

        kube_reduced = selection_formula.reduce(lambda x: To_Min_Kube_Api_Supported(x))
        subqueries = separate_formula(kube_reduced)
        subqueries_per_resource = list(product(resources, subqueries))
        total_requests = len(subqueries) * len(resources)
        logger.info(
            f"Executing {len(subqueries_per_resource)} on {len(resources)} resources"
        )
        return rx.pipe(
            rx.from_iterable(subqueries_per_resource),
            rx.flat_map(_run_on_resource_subquery),
        )
