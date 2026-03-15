from __future__ import annotations

import logging
import sys

from ..static import DEFAULT_COLORS

RESET = "\033[0m"

class CleverToolsFormatter(logging.Formatter):
    def __init__(self, fmt: str, datefmt: str | None = None, *, use_colors: bool = False) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        original_levelname = record.levelname

        if self.use_colors and sys.stdout.isatty():
            color = DEFAULT_COLORS.get(original_levelname)
            if color is not None:
                record.levelname = f"{color}{original_levelname}{RESET}"

        try:
            return super().format(record)
        finally:
            record.levelname = original_levelname

def get_logger(name: str = "clevertools") -> logging.Logger:
    return logging.getLogger(name)