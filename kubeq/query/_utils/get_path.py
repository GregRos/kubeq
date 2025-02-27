from os import path
from typing import Any
from box import Box


def get_path(b: Box, str_path: str) -> Any:
    path_list = str_path.split(".")
    for p in path_list:
        b = b[p]
    return b
