from kr8s.objects import APIObject


from dataclasses import dataclass


@dataclass
class attr_Kind:
    __match_args__ = []

    @property
    def name(self) -> str:
        return "kind"

    def get(self, object: APIObject) -> str:
        return object.kind

    def __eq__(self, other: object) -> bool:
        return isinstance(other, attr_Kind)

    def __hash__(self) -> int:
        return hash("kind")
