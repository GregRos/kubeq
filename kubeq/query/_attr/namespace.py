from box import Box
from kr8s.objects import APIObject


from dataclasses import dataclass


@dataclass
class Namespace:

    def get(self, object: object) -> str:
        match object:
            case APIObject() as o:
                return o.raw["metadata"]["namespace"]
            case Box(d):
                return d["metadata"]["namespace"]
            case _:
                raise TypeError(f"Object {object} does not have namespace")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Namespace)

    def __hash__(self) -> int:
        return hash(Namespace)

    def __str__(self) -> str:
        return "namespace"

    def __repr__(self) -> str:
        return self.__str__()
