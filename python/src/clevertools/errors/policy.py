from __future__ import annotations

from typing import TypeVar, overload
import logging

from ..configuration import ErrorMode, get_config

_LOGGER = logging.getLogger("clevertools")
T = TypeVar("T")

def _resolve_error_mode(on_error: ErrorMode | None = None) -> ErrorMode:
    if on_error is not None:
        return on_error
    return get_config().error_mode

@overload
def handle_error(exc: Exception, *, on_error: ErrorMode | None = None, fallback: T) -> T: ...


@overload
def handle_error(exc: Exception, *, on_error: ErrorMode | None = None, fallback: None = None) -> None: ...


def handle_error(exc: Exception, *, on_error: ErrorMode | None = None, fallback: T | None = None) -> T | None:
    mode = _resolve_error_mode(on_error)

    if mode == "raise":
        raise exc

    if mode == "log":
        try:
            _LOGGER.error("%s", exc)
        except Exception:
            pass

    return fallback