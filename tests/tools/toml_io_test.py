from __future__ import annotations

from clevertools.file.toml_io import read_toml, read_write

from ..paths import PATHS
from ._debug import debug


class TestTomlIO:
    def test_write_and_read_toml_roundtrip(self) -> None:
        path = PATHS.CACHE_FOLDER / "payload.toml"
        payload = {
            "project": {"name": "clevertools", "version": "0.2.1"},
            "features": {"logging": True, "masking": True},
        }

        debug(f"Schreibe TOML nach {path}")
        debug(f"TOML-Payload vor dem Schreiben: {payload}")
        read_write(path, payload, on_error="raise")

        loaded = read_toml(path, on_error="raise")
        debug(f"Geladene TOML-Daten: {loaded}")

        assert loaded == payload

    def test_read_toml_returns_none_for_missing_file_in_silent_mode(self) -> None:
        path = PATHS.CACHE_FOLDER / "missing.toml"
        if path.exists():
            path.unlink()

        debug(f"Lese absichtlich fehlende TOML-Datei: {path}")
        loaded = read_toml(path, on_error="silent")
        debug(f"Rueckgabewert fuer fehlende TOML-Datei: {loaded!r}")

        assert loaded is None