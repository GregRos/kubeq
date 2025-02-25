from itertools import groupby
from typing import Any, Iterable
from kubeq.entities._db import KubeResourceDB
from kubeq.entities._resource._resource import KubeResource
from kubeq.http._client._client import KubeClient
from kubeq.http._requests._list_request import KubeListRequest
from kubeq.logging import sources
from kubeq.query import *
from kubeq.query._attr import Label
from kubeq.query._attr.field import Field
from kubeq.query._attr.kind import Kind
import aioreactive as rx

from kubeq.query._attr.label import Label

from kubeq.run_query._kube_reductions._to_kube_api_supported import (
    Min_To_Kube_Api_Supported,
)
from kubeq.run_query.op_to_str import selector_to_kube_api
from ._kube_reductions import to_finite_set, To_Kube_Api_Supported

logger = sources.query_d.logger
