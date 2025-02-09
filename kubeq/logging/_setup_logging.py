from copy import copy
import ctypes
import logging
import sys

from colorama import Fore, Style, init

from kubeq.logging._base_source import LogSource


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = Style.DIM + Fore.WHITE
    yellow = Fore.YELLOW
    red = Fore.RED
    green = Fore.GREEN
    bold_red = Style.BRIGHT + Fore.RED
    reset = Style.RESET_ALL
    _format = "%(asctime)s %(name)s %(message)s"

    @staticmethod
    def get_formatter(string: str):
        return logging.Formatter(
            string,
            datefmt="%H:%M:%S",
        )

    formatters: dict[int, logging.Formatter] = {
        logging.DEBUG: get_formatter(f"{grey}{_format}{reset}"),
        logging.INFO: get_formatter(f"{green}{_format}{reset}"),
        logging.WARNING: get_formatter(f"{yellow}{_format}{reset}"),
        logging.ERROR: get_formatter(f"{red}{_format}{reset}"),
        logging.CRITICAL: get_formatter(f"{bold_red}{_format}{reset}"),
    }

    def format(self, record):
        c = copy(record)
        c.name = LogSource.by_name(record.name).emoji
        formatter = self.formatters[c.levelno]
        return formatter.format(c)


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
