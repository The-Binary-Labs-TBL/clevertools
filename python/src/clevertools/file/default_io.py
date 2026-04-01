from __future__ import annotations

from typing import Optional
from pathlib import Path

from ..errors.policy import handle_error
from ..configuration import ErrorMode


def read(file_path: Path | str, mode: str = "str", on_error: Optional[ErrorMode] = None) -> str | bytes | None:
    """
    Read the contents of a file as text or raw bytes.

    Args:
        file_path: Path to the file that should be read.
        mode: Read mode. Use `"str"` to return UTF-8 decoded text or
            `"bytes"` to return the raw file contents.
        on_error: Error handling mode. If omitted, the global default from
            `configure()` is used.

    Returns:
        The file contents as `str` or `bytes`, depending on `mode`. Returns
        `None` when reading fails and the selected error mode does not raise.
    """

    path = Path(file_path)

    if not path.exists():
        return handle_error(FileNotFoundError(f"File not found: {path}"), on_error=on_error, fallback=None)

    if not path.is_file():
        return handle_error(IsADirectoryError(f"Path is not a file: {path}"), on_error=on_error, fallback=None)

    try:
        if mode == "str":
            return path.read_text(encoding="utf-8")

        if mode == "bytes":
            return path.read_bytes()

        return handle_error(ValueError(f"Unsupported read mode: {mode}"), on_error=on_error, fallback=None)
    except (OSError, UnicodeDecodeError) as exc:
        return handle_error(exc, on_error=on_error, fallback=None)


def write(
    file_path: Path | str,
    data: str | bytes,
    create_if_missing: Optional[bool] = True,
    on_error: ErrorMode | None = None,
) -> None:
    """
    Write text or binary data to a file.

    Args:
        file_path: Target file path.
        data: Content to write. Use `str` for UTF-8 encoded text or `bytes`
            for binary output.
        create_if_missing: When `True`, missing parent directories are created
            automatically. When `False`, the target file must already exist.
        on_error: Error handling mode. If omitted, the global default from
            `configure()` is used.

    Returns:
        `None`. If writing fails, the outcome depends on the selected error
        mode.
    """

    path = Path(file_path)

    if not isinstance(data, (str, bytes)):
        return handle_error(TypeError(f"Text data must be a string or bytes, got {type(data).__name__}."), on_error=on_error, fallback=None)

    try:
        if create_if_missing:
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            if not path.exists():
                return handle_error(FileNotFoundError(f"File not found: {path}"), on_error=on_error, fallback=None)
            if not path.is_file():
                return handle_error(IsADirectoryError(f"Path is not a file: {path}"), on_error=on_error, fallback=None)

        if isinstance(data, str):
            path.write_text(data, encoding="utf-8")
        else:
            path.write_bytes(data)
    except OSError as exc:
        handle_error(exc, on_error=on_error, fallback=None)