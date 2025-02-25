from cProfile import label
from box import Box
from kr8s.objects import APIObject


from dataclasses import dataclass


@dataclass
class Label:
    __match_args__ = ("name",)
    name: str

    def get(self, object: object) -> str:
        match object:
            case APIObject() as o:
                return o.raw[self.name]
            case Box(d):
                return d[self.name]
            case _:
                raise TypeError(f"Object {object} does not have kind")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Label) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return f"@{self.name}"

    def __repr__(self) -> str:
        return self.__str__()
