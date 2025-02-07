from dataclasses import dataclass


@dataclass
class ResourceName:
    name: str
    plural: str
    short: tuple[str, ...]
