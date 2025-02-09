from dataclasses import dataclass
from logging import getLogger
from typing import ClassVar


@dataclass
class LogSource:
    _sources_by_name: ClassVar[dict[str, "LogSource"]] = {}
    name: str
    emoji: str

    def __new__(cls, name: str, emoji: str):
        if name in LogSource._sources_by_name:
            return LogSource._sources_by_name[name]
        source = super().__new__(cls)
        source.name = name
        source.emoji = emoji
        LogSource._sources_by_name[name] = source
        return source

    @property
    def is_kubeq(self):
        return self.name.startswith("kubeq.")

    @property
    def logger(self):
        return getLogger(self.name)

    @staticmethod
    def by_name(name: str):
        if not name.startswith("kubeq."):
            return LogSource(name, f"✳️ {name}")
        if name in LogSource._sources_by_name:
            return LogSource._sources_by_name[name]
        raise ValueError(f"Unknown log source: {name}")
