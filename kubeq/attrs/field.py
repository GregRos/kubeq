from kr8s.objects import APIObject


from dataclasses import dataclass


@dataclass
class attr_Field:
    __match_args__ = ["key"]
    name: str

    def get(self, object: APIObject) -> str:
        return getattr(object.raw, self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, attr_Field) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
