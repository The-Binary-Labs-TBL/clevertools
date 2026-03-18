from __future__ import annotations

from typing import Any, Mapping, Optional
from pathlib import Path
import tomllib

from ..errors.policy import handle_error
from ..configuration import ErrorMode


def read_toml(file_path: Path | str, on_error: Optional[ErrorMode] = None) -> dict[str, Any] | None:
    """
    Read and deserialize a TOML file.

    Args:
        file_path: Path to the TOML file that should be loaded.
        on_error: Error handling mode. If omitted, the global default from
            `configure()` is used.

    Returns:
        A dictionary representing the TOML document. Returns `None` when the
        file cannot be read or parsed and the selected error mode does not
        raise.
    """

    path = Path(file_path)

    if not path.exists():
        return handle_error(FileNotFoundError(f"File not found: {path}"), on_error=on_error, fallback=None)

    if not path.is_file():
        return handle_error(IsADirectoryError(f"Path is not a file: {path}"), on_error=on_error, fallback=None)

    try:
        with path.open("rb") as file:
            data = tomllib.load(file)

        if not isinstance(data, dict):
            return handle_error(TypeError(f"Expected TOML root to be a dictionary, got {type(data).__name__}."), on_error=on_error, fallback=None)

        return data
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return handle_error(exc, on_error=on_error, fallback=None)


def write_toml(
    file_path: Path | str,
    data: Mapping[str, Any],
    create_if_missing: Optional[bool] = True,
    on_error: ErrorMode | None = None,
) -> None:
    """
    Serialize mapping data as TOML and write it to a file.

    Args:
        file_path: Target file path.
        data: Mapping that represents the TOML document to write.
        create_if_missing: When `True`, missing parent directories are created
            automatically. When `False`, the target file must already exist.
        on_error: Error handling mode. If omitted, the global default from
            `configure()` is used.

    Returns:
        `None`. If serialization or writing fails, the outcome depends on the
        selected error mode.
    """

    path = Path(file_path)

    if not isinstance(data, Mapping):
        return handle_error(TypeError(f"TOML data must be a mapping, got {type(data).__name__}."), on_error=on_error, fallback=None)

    try:
        import tomli_w

        if create_if_missing:
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            if not path.exists():
                return handle_error(FileNotFoundError(f"TOML file not found: {path}"), on_error=on_error, fallback=None)
            if not path.is_file():
                return handle_error(IsADirectoryError(f"Path is not a file: {path}"), on_error=on_error, fallback=None)

        toml_text = tomli_w.dumps(dict(data))
        path.write_text(toml_text, encoding="utf-8")

    except (ImportError, OSError, TypeError, ValueError) as exc:
        handle_error(exc, on_error=on_error, fallback=None)
