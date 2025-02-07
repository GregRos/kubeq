from typing import Any

from box import Box


class APIResource(Box):
    def __init__(self, input: dict):
        super().__init__(input)
