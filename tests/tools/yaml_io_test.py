from __future__ import annotations

import pytest

pytest.importorskip("yaml")

from clevertools.file.yaml_io import read_yaml, write_yaml

from ..paths import PATHS
from ._debug import debug


class TestYamlIO:
    def test_write_and_read_yaml_roundtrip(self) -> None:
        path = PATHS.CACHE_FOLDER / "payload.yaml"
        payload = {
            "service": "clevertools",
            "enabled": True,
            "retries": 3,
            "labels": ["yaml", "tests", "roundtrip"],
            "profile": {"language": "Deutsch", "region": "EU"},
        }

        debug(f"Schreibe YAML nach {path}")
        debug(f"YAML-Payload vor dem Schreiben: {payload}")
        write_yaml(path, payload, on_error="raise")

        loaded = read_yaml(path, on_error="raise")
        debug(f"Geladene YAML-Daten: {loaded}")

        assert loaded == payload

    def test_read_yaml_returns_none_for_invalid_content_in_silent_mode(self) -> None:
        path = PATHS.CACHE_FOLDER / "invalid.yaml"
        path.write_text("service: clevertools\nitems: [1, 2\n", encoding="utf-8")

        debug(f"Lege absichtlich defektes YAML an: {path}")
        loaded = read_yaml(path, on_error="silent")
        debug(f"Rueckgabewert fuer defektes YAML: {loaded!r}")

        assert loaded is None

    def test_read_yaml_rejects_directory_path(self) -> None:
        path = PATHS.CACHE_FOLDER

        with pytest.raises(IsADirectoryError, match="YAML is not a file"):
            read_yaml(path, on_error="raise")

    def test_write_yaml_does_not_create_missing_file_when_disabled(self) -> None:
        path = PATHS.CACHE_FOLDER / "missing" / "blocked.yaml"
        if path.exists():
            path.unlink()

        write_yaml(path, {"blocked": True}, create_if_missing=False, on_error="silent")

        assert not path.exists()

    def test_write_yaml_rejects_none_payload(self) -> None:
        path = PATHS.CACHE_FOLDER / "none.yaml"

        with pytest.raises(ValueError, match="YAML data must not be None"):
            write_yaml(path, None, on_error="raise")