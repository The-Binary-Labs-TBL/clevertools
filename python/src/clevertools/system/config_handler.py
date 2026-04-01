from __future__ import annotations

from typing import Any, Iterator, Mapping, Optional
from pathlib import Path


from ..errors.policy import handle_error
from ..file.toml_io import read_toml
from ..file.json_io import read_json
from ..models import ErrorMode


def _deep_merge(base: dict[str, Any], incoming: Mapping[str, Any]) -> dict[str, Any]:
    for key, value in incoming.items():
        current = base.get(key)

        if isinstance(current, dict) and isinstance(value, Mapping):
            base[key] = _deep_merge(dict(current), value)
            continue

        if isinstance(value, Mapping):
            base[key] = _deep_merge({}, value)
            continue

        base[key] = value

    return base


class ConfigNode:
    def __init__(self, data: Mapping[str, Any]) -> None:
        self._data = dict(data)

    def __getattr__(self, name: str) -> Any:
        try:
            value = self._data[name]
        except KeyError as exc:
            raise AttributeError(f"Config key not found: {name}") from exc
        return self._wrap(value)

    def __getitem__(self, key: str) -> Any:
        return self._wrap(self._data[key])

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data!r})"

    def as_dict(self) -> dict[str, Any]:
        return _to_plain_dict(self._data)

    def get(self, path: str, default: Any = None) -> Any:
        current: Any = self

        for part in path.split("."):
            if not part:
                return default

            if isinstance(current, ConfigNode):
                if part not in current:
                    return default
                current = current[part]
                continue

            if isinstance(current, Mapping):
                if part not in current:
                    return default
                current = current[part]
                continue

            return default

        return current

    @staticmethod
    def _wrap(value: Any) -> Any:
        if isinstance(value, Mapping):
            return ConfigNode(value)
        return value


def _to_plain_dict(data: Mapping[str, Any]) -> dict[str, Any]:
    plain: dict[str, Any] = {}

    for key, value in data.items():
        if isinstance(value, Mapping):
            plain[key] = _to_plain_dict(value)
            continue
        plain[key] = value

    return plain


class ConfigHandler(ConfigNode):
    @classmethod
    def load(cls, *paths: Path | str, on_error: Optional[ErrorMode] = None) -> ConfigHandler:
        merged: dict[str, Any] = {}
        loaded: Mapping[str, Any] | None = None

        for path in paths:
            suffix = Path(path).suffix.lower()

            if suffix == ".toml":
                loaded = read_toml(path, on_error=on_error)
            elif suffix == ".json":
                loaded = read_json(path, on_error=on_error)
            elif suffix in {".yaml", ".yml"}:
                try:
                    from ..file.yaml_io import read_yaml
                except ImportError as exc:
                    loaded = handle_error(exc, on_error=on_error, fallback=None)
                else:
                    loaded = read_yaml(path, on_error=on_error)
            else:
                loaded = handle_error(
                    ValueError("Invalid config handler type! Only .toml, .json and .yaml(.yml) file types are allowed"),
                    on_error=on_error,
                    fallback=None,
                )

            if loaded is None:
                continue

            if not isinstance(loaded, Mapping):
                loaded = handle_error(
                    TypeError(f"Config root must be a mapping, got {type(loaded).__name__}."),
                    on_error=on_error,
                    fallback=None,
                )
                if loaded is None:
                    continue

            merged = _deep_merge(merged, loaded)

        return cls(merged)


def load_config(*file_paths: Path | str, on_error: Optional[ErrorMode] = None) -> ConfigHandler:
    """
    Load and merge one or more configuration files into a `ConfigHandler`.

    Supported file types are TOML, JSON, YAML, and YML. Files are processed in
    the order they are provided, and later files override earlier values while
    nested mappings are merged recursively.

    Args:
        file_paths: One or more paths to configuration files.
        on_error: Error handling mode. If omitted, the configured default is
            used.

    Returns:
        A `ConfigHandler` that provides attribute and key-based access to the
        merged configuration data.
    """
    return ConfigHandler.load(*file_paths, on_error=on_error)