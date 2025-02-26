from dataclasses import dataclass

from kubeq.entities._resource._resource import KubeResource
import kubeq.query._attr as _attr
import kubeq.query._operators as oprs
from kubeq.selection._selector import Selector


type InstanceSelector = Selector[_attr.Api]
