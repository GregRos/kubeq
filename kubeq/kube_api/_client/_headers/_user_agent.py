import os
import platform
from kubeq.version import __version__


def _get_os() -> str:
    pt = platform.system().lower()
    if pt == "darwin":
        return "macos"
    return pt


def _get_arch() -> str:
    return platform.machine().lower()


def get_user_agent() -> str:
    os = _get_os()
    arch = _get_arch()
    package = __package__
    version = __version__
    return f"{package}/v{version} {os}/{arch}"
