from __future__ import annotations

from pathlib import Path

from ..errors.policy import handle_error
from ..configuration import ErrorMode


def read(file_path: Path | str, on_error: ErrorMode | None = None) -> str | None:
    """
    Read a file as UTF-8 text without applying format-specific parsing.

    This helper is intended for simple text-based files such as `.txt`, `.env`,
    or templates where the raw content should be returned exactly as stored.

    Args:
        file_path: Path to the file that should be read.
        on_error: Error handling mode. Use `"raise"` to re-raise the exception,
            `"log"` to log the error and return `None`, or `"silent"` to return
            `None` without logging.

    Returns:
        The file content as a string, or `None` when reading fails and the
        selected error mode does not raise.
    """

    path = Path(file_path)

    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        return handle_error(exc, on_error=on_error, fallback=None)


def write(file_path: Path | str, data: str, on_error: ErrorMode | None = None) -> None:
    """
    Write UTF-8 text to a file without using a format-specific serializer.

    This helper is intended for plain files such as `.txt`, `.env`, or small
    generated assets where the content should be written exactly as provided.

    Args:
        file_path: Path to the target file.
        data: Raw text content to write.
        on_error: Error handling mode. Use `"raise"` to re-raise the exception,
            `"log"` to log the error, or `"silent"` to suppress the exception.
    """

    path = Path(file_path)

    try:
        path.write_text(data, encoding="utf-8")
    except Exception as exc:
        handle_error(exc, on_error=on_error, fallback=None)