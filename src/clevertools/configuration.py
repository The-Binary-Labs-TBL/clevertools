from __future__ import annotations

from dataclasses import replace
from threading import RLock
from typing import Any

from .static import CleverToolsConfig, ErrorMode

_LOCK = RLock()
_CONFIG = CleverToolsConfig()

def _validate_error_mode(mode: ErrorMode) -> ErrorMode:
    if mode not in ("raise", "log", "silent"):
        raise ValueError(f"Unsupported error_mode: {mode!r}")
    return mode

def get_config() -> CleverToolsConfig:
    with _LOCK:
        return replace(_CONFIG)

def configure(
    *,
    error_mode: ErrorMode | None = None,
    logger_overrides: dict[str, Any] | None = None,
) -> CleverToolsConfig:
    """
    Configure global defaults for `clevertools`.

    Args:
        error_mode: Default error handling mode used by helpers that support
            `on_error`.
        logger_overrides: Default keyword arguments used by
            `configure_logger()`.

    Returns:
        A copy of the active configuration after applying the update.
    """

    global _CONFIG

    with _LOCK:
        next_config = _CONFIG

        if error_mode is not None:
            next_config = replace(
                next_config,
                error_mode=_validate_error_mode(error_mode),
            )

        if logger_overrides is not None:
            next_config = replace(
                next_config,
                logger_overrides=dict(logger_overrides),
            )

        _CONFIG = next_config

        return replace(_CONFIG)
