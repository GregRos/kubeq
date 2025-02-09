from dataclasses import dataclass, field


@dataclass
class CacheKey:
    domain: str

    key: str = field(init=False)
