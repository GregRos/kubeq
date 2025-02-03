from dataclasses import dataclass
from kr8s import objects

@dataclass
class ApiKindSelector:
    kind: str


@dataclass
class ApiLabelSelector:
    key: str
    value: str
    
@dataclass
class PostApiSelector: