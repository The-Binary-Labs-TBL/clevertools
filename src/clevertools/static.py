from __future__ import annotations

from typing import Dict, Any, Literal
from dataclasses import dataclass, field

ErrorMode = Literal["raise", "log", "silent"]
WriteMode = Literal["runtime", "buffered"]

DEFAULT_LOGGER_NAME = "clevertools"
DEFAULT_RECORD_FORMAT = "%(name)s | [%(levelname)s] %(message)s"
DEFAULT_STRUCTURE_FORMAT = "%(asctime)s | %(name)s | [%(levelname)s] %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_TIME_FORMAT = "%H:%M:%S"
DEFAULT_DATETIME_FORMAT = f"{DEFAULT_DATE_FORMAT} {DEFAULT_TIME_FORMAT}"

DEFAULT_COLORS = {
    "INFO": "\033[36m",
    "DEBUG": "\033[37m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[35m",
}

@dataclass(frozen=True)
class CleverToolsConfig:
    error_mode: ErrorMode = "log"
    logger_overrides: Dict[str, Any] = field(default_factory=dict)
