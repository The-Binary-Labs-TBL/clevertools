from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..models import (
    DEFAULT_FORMAT,
    DEFAULT_FORMAT_EXTENTED,
    ResolvedLoggerOptions,
    WriteMode,
    LoggerFormatPreset,
)
from ..configuration import get_config

def resolve_logger_options(
    *,
    level: int | str | None,
    format_preset: LoggerFormatPreset | None,
    fmt: str | None,
    date_format: str | None,
    console_enabled: bool | None,
    file_logging_enabled: bool | None,
    file_log_path: str | Path | None,
    file_write_mode: WriteMode,
    use_colors: bool,
) -> ResolvedLoggerOptions:
    config = get_config()
    overrides = dict(config.logger_overrides)

    resolved_level = _take_override(overrides, "level", level, "INFO")
    resolved_format_preset = _take_override(
        overrides,
        "format_preset",
        format_preset,
        "default",
    )
    resolved_console_enabled = _take_override(
        overrides,
        "console_enabled",
        console_enabled,
        True,
    )
    resolved_file_logging_enabled = _take_override(
        overrides,
        "file_logging_enabled",
        file_logging_enabled,
        False,
    )
    resolved_file_log_path = _take_override(
        overrides,
        "file_log_path",
        file_log_path,
        None,
    )
    resolved_date_format = _take_override(overrides, "date_format", date_format, None)
    resolved_fmt = _take_override(overrides, "fmt", fmt, None)

    if resolved_fmt is None:
        resolved_fmt = _resolve_default_format(resolved_format_preset)

    return ResolvedLoggerOptions(
        level=resolved_level,
        format_preset=resolved_format_preset,
        fmt=resolved_fmt,
        date_format=resolved_date_format,
        console_enabled=resolved_console_enabled,
        file_logging_enabled=resolved_file_logging_enabled,
        file_log_path=resolved_file_log_path,
        file_write_mode=file_write_mode,
        use_colors=use_colors,
    )

def _take_override(overrides: dict[str, Any], key: str, explicit_value: Any, default_value: Any) -> Any:
    if explicit_value is not None:
        return explicit_value

    return overrides.pop(key, default_value)


def _resolve_default_format(format_preset: LoggerFormatPreset) -> str:
    if format_preset == "datetime":
        return DEFAULT_FORMAT_EXTENTED

    return DEFAULT_FORMAT