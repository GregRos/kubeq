from dataclasses import dataclass
from typing import Iterable, TypedDict

from kubeq import attr
from kubeq.selection.selector import Selector
from kubeq.selection_str.to_selector_str import to_selector_str
