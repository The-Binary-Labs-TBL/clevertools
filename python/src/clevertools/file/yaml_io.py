from __future__ import annotations

from typing import Any, Optional
from pathlib import Path
import yaml  # type: ignore[import-untyped]

from ..errors.exceptions import YamlReadError, YamlWriteError
from ..errors.policy import handle_error
from ..configuration import ErrorMode


def read_yaml(file_path: Path | str, on_error: Optional[ErrorMode] = None) -> Any | None:
    """
    Read and deserialize a YAML file.

    Args:
        file_path: Path to the YAML file that should be loaded.
        on_error: Error handling mode. If omitted, the global default from
            `configure()` is used.

    Returns:
        The parsed YAML value. Returns `None` when the file cannot be read or
        parsed and the selected error mode does not raise.
    """

    path = Path(file_path)

    if not path.exists():
        return handle_error(FileNotFoundError(f"YAML file not found: {path}"), on_error=on_error, fallback=None)

    if not path.is_file():
        return handle_error(IsADirectoryError(f"YAML is not a file: {path}"), on_error=on_error, fallback=None)

    try:
        with path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        return handle_error(YamlReadError(f"Invalid YAML format: {e}"), on_error=on_error, fallback=None)
    except Exception as e:
        return handle_error(YamlReadError(f"Failed to read YAML: {e}"), on_error=on_error, fallback=None)

def write_yaml(
    file_path: Path | str,
    data: Any,
    create_if_missing: Optional[bool] = True,
    allow_unicode: bool = True,
    sort_keys: bool = False,
    on_error: ErrorMode | None = None,
) -> None:
    """
    Serialize data as YAML and write it to a file.

    Args:
        file_path: Target file path.
        data: YAML-serializable value to write.
        create_if_missing: When `True`, missing parent directories are created
            automatically. When `False`, the target file must already exist.
        allow_unicode: Forwarded to `yaml.safe_dump()` to control whether
            Unicode characters are emitted directly.
        sort_keys: Forwarded to `yaml.safe_dump()` to control whether mapping
            keys are sorted in the output.
        on_error: Error handling mode. If omitted, the global default from
            `configure()` is used.

    Returns:
        `None`. If serialization or writing fails, the outcome depends on the
        selected error mode.
    """

    path = Path(file_path)

    if data is None:
        return handle_error(ValueError("YAML data must not be None."), on_error=on_error, fallback=None)

    try:
        if create_if_missing:
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            if not path.exists():
                return handle_error(FileNotFoundError(f"YAML file not found: {path}"), on_error=on_error, fallback=None)
            
            if not path.is_file():
                return handle_error(IsADirectoryError(f"YAML is not a file: {path}"), on_error=on_error, fallback=None)

        with path.open("w", encoding="utf-8") as file:
            yaml.safe_dump(data, file, allow_unicode=allow_unicode, sort_keys=sort_keys)
    except yaml.YAMLError as e:
        return handle_error(YamlWriteError(f"Invalid YAML data: {e}"), on_error=on_error, fallback=None)
    except Exception as e:
        return handle_error(YamlWriteError(f"Failed to write YAML: {e}"), on_error=on_error, fallback=None)