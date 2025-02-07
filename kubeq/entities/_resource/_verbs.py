from typing import Literal


type KubeVerb = Literal[
    "get", "list", "watch", "create", "update", "patch", "delete", "deletecollection"
]
type Verbs = tuple[KubeVerb, ...]
