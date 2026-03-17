from __future__ import annotations

from pathlib import Path
import logging

from ..models import (
    DEFAULT_LOGGER_NAME,
    LoggerFormatPreset,
    WriteMode,
)
from .handlers import build_console_handler, build_file_handler, reset_handlers
from .options import resolve_logger_options
from .logger import get_logger


def configure_logger(
    *,
    name: str = DEFAULT_LOGGER_NAME,
    level: int | str | None = None,
    format_preset: LoggerFormatPreset | None = None,
    fmt: str | None = None,
    date_format: str | None = None,
    console_enabled: bool | None = None,
    file_logging_enabled: bool | None = None,
    file_log_path: str | Path | None = None,
    file_write_mode: WriteMode = "runtime",
    use_colors: bool = True,
) -> logging.Logger:
    options = resolve_logger_options(
        level=level,
        format_preset=format_preset,
        fmt=fmt,
        date_format=date_format,
        console_enabled=console_enabled,
        file_logging_enabled=file_logging_enabled,
        file_log_path=file_log_path,
        file_write_mode=file_write_mode,
        use_colors=use_colors,
    )

    logger = get_logger(name)
    logger.setLevel(options.level)
    logger.propagate = False

    reset_handlers(logger)

    if options.console_enabled:
        logger.addHandler(build_console_handler(options))

    if options.file_logging_enabled:
        logger.addHandler(build_file_handler(options))

    return logger