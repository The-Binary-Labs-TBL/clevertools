from __future__ import annotations

from typing import TextIO
from pathlib import Path
import logging

from .formatter import CleverToolsFormatter
from .options import ResolvedLoggerOptions
from ..models import WriteMode


def reset_handlers(logger: logging.Logger) -> None:
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()


def build_console_handler(
    options: ResolvedLoggerOptions,
    stream: TextIO | None = None,
) -> logging.Handler:
    console_handler = logging.StreamHandler(stream)
    console_handler.setFormatter(
        CleverToolsFormatter(
            options.fmt,
            datefmt=options.date_format,
            use_colors=options.use_colors,
        )
    )
    return console_handler


def build_file_handler(options: ResolvedLoggerOptions) -> logging.Handler:
    log_path = Path(options.file_log_path or "clevertools.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(
        log_path,
        mode=file_mode(options.file_write_mode),
        encoding="utf-8",
    )
    file_handler.setFormatter(
        CleverToolsFormatter(
            options.fmt,
            datefmt=options.date_format,
        )
    )
    return file_handler


def file_mode(file_write_mode: WriteMode) -> str:
    return "w" if file_write_mode == "runtime" else "a"