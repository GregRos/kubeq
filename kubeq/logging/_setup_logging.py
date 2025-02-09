from copy import copy
import ctypes
import logging
import sys
from typing import Any, Iterable

from colorama import Fore, Style, init
import termcolor

from kubeq.logging._base_source import LogSource


def _style(level: int, heading: bool, text: str):
    attrs: Iterable[Any] = ["bold"] if heading else []
    styles = {
        logging.DEBUG: lambda x: termcolor.colored(x, "grey", attrs=attrs),
        logging.INFO: lambda x: termcolor.colored(x, "green", attrs=attrs),
        logging.WARNING: lambda x: termcolor.colored(x, "yellow", attrs=attrs),
        logging.ERROR: lambda x: termcolor.colored(x, "light_red", attrs=attrs),
        logging.CRITICAL: lambda x: termcolor.colored(
            x, "black", on_color="on_light_red", attrs=attrs
        ),
    }
    return styles[level](text)


def _get_formatter(level: int):
    _format = "%(asctime)s %(name)s %(message)s"
    styled = _style(level, True, _format)
    return logging.Formatter(
        styled,
        datefmt="%H:%M:%S",
    )


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    def _format_args(self, record: logging.LogRecord) -> Iterable[str]:
        match record.args:
            case None:
                return []
            case tuple(args):
                return [f"  ∙ {str(a)}" for a in args]
            case dict(args):
                return [f"    {k} = {v}" for k, v in args.items()]
            case _:
                raise ValueError("Invalid type")

    def format(self, record):
        c = copy(record)
        c.name = LogSource.by_name(record.name).emoji
        formatter = _get_formatter(record.levelno)

        line1 = formatter.format(c)
        rest = self._format_args(c)
        all_lines = [_style(record.levelno, False, r) for r in rest]
        all_lines = [line1, *all_lines]
        return "\n".join(all_lines) + "\n"


def _filter_out_internal_debug(record: logging.LogRecord):
    return LogSource.by_name(record.name).is_kubeq


def setup_logging(minLevel: int = logging.DEBUG):
    print("Setting up logging")
    init(autoreset=True)
    handlers: list[logging.StreamHandler] = [
        logging.FileHandler("log.log", encoding="utf-8"),
        logging.StreamHandler(),
    ]
    root_logger = logging.getLogger()
    root_logger.setLevel(minLevel)
    for h in handlers:
        h.addFilter(_filter_out_internal_debug)
        h.setFormatter(CustomFormatter())
        h.setLevel(minLevel)
        root_logger.addHandler(h)
