from __future__ import annotations

from typing import Any, Iterator, Mapping
from pathlib import Path

from ..file.toml_io import read_toml


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
    """Small wrapper that exposes nested configuration keys via attributes."""

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
        """Return the wrapped configuration as a plain nested dictionary."""
        return _to_plain_dict(self._data)

    def get(self, path: str, default: Any = None) -> Any:
        """Read a value via dot-path notation and return `default` if it is missing."""
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
    """Load and expose multiple TOML files as one merged configuration tree."""

    @classmethod
    def load(cls, *file_paths: Path | str) -> "ConfigHandler":
        """
        Read multiple TOML files and merge them into one config object.

        Nested tables are merged recursively. When the same non-mapping key
        exists in multiple files, the value from the later file wins.
        """
        merged: dict[str, Any] = {}

        for file_path in file_paths:
            loaded = read_toml(file_path, on_error="raise")
            if loaded is None:
                continue
            merged = _deep_merge(merged, loaded)

        return cls(merged)


def load_config(*file_paths: Path | str) -> ConfigHandler:
    """
    Load multiple TOML files and expose them as one merged config object.

    Files are processed in the given order. Nested TOML tables are merged
    recursively so related sections from separate files appear together in the
    final result. If the same non-mapping key appears in multiple files, the
    value from the later file replaces the earlier one.

    The returned object supports attribute-style access for nested sections and
    `get()` for dot-path lookup.
    """
    return ConfigHandler.load(*file_paths)