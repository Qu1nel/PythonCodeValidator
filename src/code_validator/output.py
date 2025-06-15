import logging
import sys
from typing import Literal

from .config import LogLevel

LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(log_level: LogLevel) -> logging.Logger:
    logging.basicConfig(level=log_level, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    return logging.getLogger()


class Console:
    def __init__(self, logger: logging.Logger, *, is_silent: bool = False):
        self._logger = logger
        self._is_silent = is_silent
        self._stdout = sys.stdout

    def print(
        self,
        message: str,
        *,
        level: LogLevel | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = LogLevel.INFO,
    ) -> None:
        log_method = getattr(self._logger, level.value.lower() if isinstance(level, LogLevel) else level.lower())
        log_method(message)

        if not self._is_silent:
            print(message, file=self._stdout)
