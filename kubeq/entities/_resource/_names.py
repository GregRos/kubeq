from dataclasses import dataclass

from box import Box


@dataclass
class KubeNames:
    main: str
    plural: str
    short: tuple[str, ...]
