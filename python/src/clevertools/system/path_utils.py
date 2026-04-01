from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from ..errors.exceptions import FileSystemError, ValidationError
from ..errors.policy import handle_error
from ..file.default_io import write
from ..models import ErrorMode

def _normalize_paths(paths: Path | str | List[Path | str], on_error: Optional[ErrorMode] = None) -> List[Path] | None:
    """Normalize supported path inputs into a list of ``Path`` objects."""

    if isinstance(paths, (Path, str)):
        return [Path(paths)]

    if isinstance(paths, list):
        if not all(isinstance(path, (Path, str)) for path in paths):
            return handle_error(ValidationError("'All entries in 'paths' must be of type 'str' or 'Path'."), on_error=on_error, fallback=None)
        return [Path(path) for path in paths]

    return handle_error(ValidationError("'paths' must be a 'str', 'Path', or a list of those values."), on_error=on_error, fallback=None)


def ensure_file(
    paths: Path | str | List[Path | str],
    default_content: str | bytes = "No default content was provided for the new file.",
    replace: bool = False,
    on_error: Optional[ErrorMode] = None,
) -> None:
    """
    Ensure that one or more file paths exist and point to regular files.

    This helper accepts a single path or a list of paths. Missing parent
    directories are created automatically. When ``replace`` is ``False``,
    missing files are created as empty files and existing files are left
    unchanged. When ``replace`` is ``True``, the helper writes
    ``default_content`` to each target file using the shared default file
    writer.

    Args:
        paths: A single file path or a list of file paths.
        default_content: Text or binary content to write when ``replace`` is
            enabled.
        replace: When ``True``, overwrite each target file with
            ``default_content``. When ``False``, only ensure that the file
            exists.
        on_error: Error handling mode. If omitted, the configured package
            default is used.

    Returns:
        ``None``. If a path is invalid or a filesystem operation fails, the
        outcome depends on the selected error mode.
    """

    try:
        items = _normalize_paths(paths, on_error)
        if items is None:
            return

        for item in items:
            if item.exists() and not item.is_file():
                return handle_error(ValidationError(f"Expected a file path, but got a directory: {item}"), on_error=on_error, fallback=None)

            item.parent.mkdir(parents=True, exist_ok=True)

            if replace:
                write(item, default_content, on_error=on_error)
                continue

            if not item.exists():
                item.touch(exist_ok=True)
    except OSError as exc:
        handle_error(FileSystemError(str(exc)), on_error=on_error, fallback=None)
    except ValidationError as exc:
        handle_error(exc, on_error=on_error, fallback=None)


def ensure_dir(paths: Path | str | List[Path | str], on_error: Optional[ErrorMode] = None) -> None:
    """
    Ensure that one or more directory paths exist and point to directories.

    This helper accepts a single path or a list of paths. Missing directories
    are created recursively. Existing directories are left unchanged. If a
    target path already exists as a file, the helper follows the shared error
    policy.

    Args:
        paths: A single directory path or a list of directory paths.
        on_error: Error handling mode. If omitted, the configured package
            default is used.

    Returns:
        ``None``. If a path is invalid or directory creation fails, the outcome
        depends on the selected error mode.
    """

    try:
        items = _normalize_paths(paths, on_error)
        if items is None:
            return

        for item in items:
            if item.exists() and not item.is_dir():
                return handle_error(ValidationError(f"Expected a directory path, but got a file: {item}"), on_error=on_error, fallback=None)
            
            item.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        handle_error(FileSystemError(str(exc)), on_error=on_error, fallback=None)
    except ValidationError as exc:
        handle_error(exc, on_error=on_error, fallback=None)