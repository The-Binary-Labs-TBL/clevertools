from __future__ import annotations

import logging

from ..models import DEFAULT_LOGGER_NAME

def get_logger(name: str = DEFAULT_LOGGER_NAME) -> logging.Logger:
    return logging.getLogger(name)