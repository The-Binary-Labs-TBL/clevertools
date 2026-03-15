from __future__ import annotations

from pathlib import Path
import logging

from ..static import (
    DEFAULT_DATETIME_FORMAT,
    DEFAULT_LOGGER_NAME,
    DEFAULT_RECORD_FORMAT,
    DEFAULT_STRUCTURE_FORMAT,
    WriteMode,
)
from .logger import CleverToolsFormatter, get_logger
from ..configuration import get_config

def configure_logger(
    *,
    name: str = DEFAULT_LOGGER_NAME,
    level: int | str | None = None,
    fmt: str | None = None,
    date_format: str | None = None,
    console_enabled: bool | None = None,
    file_logging_enabled: bool | None = None,
    file_log_path: str | Path | None = None,
    file_write_mode: WriteMode = "runtime",
    use_colors: bool = True,
) -> logging.Logger:
    config = get_config()
    overrides = dict(config.logger_overrides)

    resolved_level = overrides.pop("level", "INFO") if level is None else level
    resolved_console_enabled = (
        overrides.pop("console_enabled", True)
        if console_enabled is None
        else console_enabled
    )
    resolved_file_logging_enabled = (
        overrides.pop("file_logging_enabled", False)
        if file_logging_enabled is None
        else file_logging_enabled
    )
    resolved_file_log_path = (
        overrides.pop("file_log_path", None)
        if file_log_path is None
        else file_log_path
    )
    resolved_date_format = (
        overrides.pop("date_format", DEFAULT_DATETIME_FORMAT)
        if date_format is None
        else date_format
    )
    resolved_fmt = overrides.pop("fmt", None) if fmt is None else fmt

    if resolved_fmt is None:
        resolved_fmt = (
            DEFAULT_STRUCTURE_FORMAT
            if resolved_file_logging_enabled
            else DEFAULT_RECORD_FORMAT
        )

    logger = get_logger(name)
    logger.setLevel(resolved_level)
    logger.propagate = False

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    formatter = CleverToolsFormatter(
        resolved_fmt,
        datefmt=resolved_date_format,
        use_colors=use_colors,
    )

    if resolved_console_enabled:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if resolved_file_logging_enabled:
        if resolved_file_log_path is None:
            resolved_file_log_path = Path("clevertools.log")

        log_path = Path(resolved_file_log_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        mode = "w" if file_write_mode == "runtime" else "a"
        file_handler = logging.FileHandler(log_path, mode=mode, encoding="utf-8")
        file_handler.setFormatter(
            CleverToolsFormatter(resolved_fmt, datefmt=resolved_date_format)
        )
        logger.addHandler(file_handler)

    return logger