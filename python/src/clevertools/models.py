from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, Literal
from pathlib import Path
from typing import Any

ErrorMode = Literal["raise", "log", "silent"]
WriteMode = Literal["runtime", "buffered"]
LoggerFormatPreset = Literal["default", "datetime"]

DEFAULT_LOGGER_NAME = "clevertools"
DEFAULT_FORMAT_EXTENTED = "%(name)s | %(levelname)s | [%(date)s] [%(time)s] = %(message)s"
DEFAULT_FORMAT = "%(name)s | [%(levelname)s] = %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_TIME_FORMAT = "%H:%M:%S"
RESET = "\033[0m"

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


@dataclass(frozen=True)
class ResolvedLoggerOptions:
    level: int | str
    format_preset: LoggerFormatPreset
    fmt: str
    date_format: str
    console_enabled: bool
    file_logging_enabled: bool
    file_log_path: str | Path | None
    file_write_mode: WriteMode
    use_colors: bool