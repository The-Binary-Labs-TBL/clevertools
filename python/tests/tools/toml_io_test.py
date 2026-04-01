from __future__ import annotations

from clevertools.file.toml_io import read_toml, write_toml
from pathlib import Path
import pytest

pytest.importorskip("tomli_w")

from ._debug import debug

def test_write_and_read_toml_roundtrip(cache_dir: Path) -> None:
    path = cache_dir / "payload.toml"
    payload = {
        "project": {"name": "clevertools", "version": "0.2.1"},
        "features": {"logging": True, "masking": True},
    }

    debug(f"Schreibe TOML nach {path}")
    debug(f"TOML-Payload vor dem Schreiben: {payload}")
    write_toml(path, payload, on_error="raise")

    loaded = read_toml(path, on_error="raise")
    debug(f"Geladene TOML-Daten: {loaded}")

    assert loaded == payload


def test_read_toml_returns_none_for_missing_file_in_silent_mode(cache_dir: Path) -> None:
    path = cache_dir / "missing.toml"
    debug(f"Lese absichtlich fehlende TOML-Datei: {path}")
    loaded = read_toml(path, on_error="silent")
    debug(f"Rueckgabewert fuer fehlende TOML-Datei: {loaded!r}")

    assert loaded is None


def test_read_toml_rejects_directory_path(cache_dir: Path) -> None:
    with pytest.raises(IsADirectoryError, match="Path is not a file"):
        read_toml(cache_dir, on_error="raise")


def test_write_toml_does_not_create_missing_file_when_disabled(cache_dir: Path) -> None:
    path = cache_dir / "missing" / "blocked.toml"
    write_toml(path, {"blocked": True}, create_if_missing=False, on_error="silent")

    assert not path.exists()


def test_write_toml_rejects_non_mapping_payload(cache_dir: Path) -> None:
    path = cache_dir / "invalid.toml"

    with pytest.raises(TypeError, match="TOML data must be a mapping"):
        write_toml(path, ["not", "a", "mapping"], on_error="raise")  # type: ignore[arg-type]
