from __future__ import annotations

from typing import Any, Optional
from pathlib import Path
import json

from ..errors.policy import handle_error
from ..configuration import ErrorMode


def read_json(file_path: Path | str, on_error: Optional[ErrorMode] = None) -> Any | None:
    """
    Read and deserialize a JSON file.

    Args:
        file_path: Path to the JSON file that should be loaded.
        on_error: Error handling mode. If omitted, the global default from
            `configure()` is used.

    Returns:
        The parsed JSON value. Returns `None` when the file cannot be read or
        parsed and the selected error mode does not raise.
    """

    path = Path(file_path)

    if not path.exists():
        return handle_error(FileNotFoundError(f"JSON file not found: {path}"), on_error=on_error, fallback=None)

    if not path.is_file():
        return handle_error(IsADirectoryError(f"Path is not a file: {path}"), on_error=on_error, fallback=None)

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return handle_error(exc, on_error=on_error, fallback=None)


def write_json(
    file_path: Path | str,
    data: Any,
    create_if_missing: Optional[bool] = True,
    ensure_ascii: bool = True,
    indent: int = 4,
    on_error: ErrorMode | None = None,
) -> None:
    """
    Serialize data as JSON and write it to a file.

    Args:
        file_path: Target file path.
        data: JSON-serializable value to write.
        create_if_missing: When `True`, missing parent directories are created
            automatically. When `False`, the target file must already exist.
        ensure_ascii: Forwarded to `json.dump()` to control whether non-ASCII
            characters are escaped.
        indent: Indentation level used for the formatted JSON output.
        on_error: Error handling mode. If omitted, the global default from
            `configure()` is used.

    Returns:
        `None`. If serialization or writing fails, the outcome depends on the
        selected error mode.
    """

    path = Path(file_path)

    if data is None:
        return handle_error(ValueError("JSON data must not be None."), on_error=on_error, fallback=None)

    try:
        if create_if_missing:
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            if not path.exists():
                return handle_error(FileNotFoundError(f"JSON file not found: {path}"), on_error=on_error, fallback=None)
            if not path.is_file():
                return handle_error(IsADirectoryError(f"Path is not a file: {path}"), on_error=on_error, fallback=None)

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=ensure_ascii, indent=indent)
    except (OSError, TypeError, ValueError) as exc:
        handle_error(exc, on_error=on_error, fallback=None)