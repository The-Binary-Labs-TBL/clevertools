from __future__ import annotations

from typing import Any, Optional
from pathlib import Path
import toml

from ..errors.policy import handle_error
from ..configuration import ErrorMode

def read_toml(file_path: Path | str, on_error: Optional[ErrorMode] = None) -> Any | None:
    """
    Read TOML data from a UTF-8 encoded file.

    The file content is parsed with the `toml` library and returned as the
    corresponding Python value, typically a dictionary with nested structures
    such as lists, strings, numbers, and booleans.

    Args:
        file_path: Path to the TOML file that should be read.
        on_error: Error handling mode. Use `"raise"` to re-raise the exception,
            `"log"` to log the error and return `None`, or `"silent"` to return
            `None` without logging.

    Returns:
        The parsed TOML value, or `None` when the file cannot be read or the
        content cannot be parsed and the
        selected error mode does not raise.
    """

    path = Path(file_path)
    
    if not path.exists():
        return handle_error(Exception(f"File not found: {path}") ,on_error=on_error, fallback=None)

    try:
        return toml.load(path)
    except Exception as exc:
        return handle_error(exc, on_error=on_error, fallback=None)

def read_write(
    file_path: Path | str,
    data: Any,
    create_if_missing: Optional[bool] = True,
    on_error: ErrorMode | None = None
) -> None:
    """
    Serialize a Python value to TOML and write it as UTF-8 text.

    The given value should be compatible with TOML serialization, typically a
    dictionary containing supported TOML value types. This helper currently
    treats `None` as invalid input. Depending on `create_if_missing`, the
    target file can either be created automatically or must already exist.

    Args:
        file_path: Path to the target TOML file.
        data: Python value to serialize and write as TOML.
        create_if_missing: Whether to create the target file if it does not
            already exist. If set to `False`, writing fails when the file is
            missing.
        on_error: Error handling mode. Use `"raise"` to re-raise the exception,
            `"log"` to log the error, or `"silent"` to suppress the exception.

    Returns:
        `None`. If an error occurs and the selected error mode does not raise,
        the function handles it according to `on_error`.
    """

    path = Path(file_path)

    if not create_if_missing and not path.exists():
        return handle_error(Exception(f"File not found: {path}"), on_error=on_error, fallback=None)

    if data is None:
        return handle_error(Exception(f"Data is not valid!") ,on_error=on_error, fallback=None)

    try:
        path.write_text(toml.dumps(data), encoding="utf-8")
    except Exception as exc:
        handle_error(exc, on_error=on_error, fallback=None)