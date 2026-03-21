from __future__ import annotations

from clevertools.file.json_io import read_json, write_json
from pathlib import Path
import pytest

from ._debug import debug

def test_write_and_read_json_roundtrip(cache_dir: Path) -> None:
    path = cache_dir / "payload.json"
    payload = {
        "service": "clevertools",
        "enabled": True,
        "retries": 3,
        "tags": ["debug", "tests", "json"],
    }

    debug(f"Schreibe JSON nach {path}")
    debug(f"JSON-Payload vor dem Schreiben: {payload}")
    write_json(path, payload, on_error="raise")

    loaded = read_json(path, on_error="raise")
    debug(f"Geladene JSON-Daten: {loaded}")

    assert loaded == payload


def test_read_json_returns_none_for_invalid_content_in_silent_mode(cache_dir: Path) -> None:
    path = cache_dir / "invalid.json"
    path.write_text("{ invalid json", encoding="utf-8")

    debug(f"Lege absichtlich defektes JSON an: {path}")
    loaded = read_json(path, on_error="silent")
    debug(f"Rueckgabewert fuer defektes JSON: {loaded!r}")

    assert loaded is None


def test_read_json_rejects_directory_path(cache_dir: Path) -> None:
    with pytest.raises(IsADirectoryError, match="Path is not a file"):
        read_json(cache_dir, on_error="raise")


def test_write_json_does_not_create_missing_file_when_disabled(cache_dir: Path) -> None:
    path = cache_dir / "missing" / "blocked.json"
    write_json(path, {"blocked": True}, create_if_missing=False, on_error="silent")

    assert not path.exists()


def test_write_json_rejects_none_payload(cache_dir: Path) -> None:
    path = cache_dir / "none.json"

    with pytest.raises(ValueError, match="JSON data must not be None"):
        write_json(path, None, on_error="raise")