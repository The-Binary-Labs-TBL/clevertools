from __future__ import annotations

from clevertools.file.json_io import read_json, write_json

from ..paths import PATHS
from ._debug import debug


class TestJsonIO:
    def test_write_and_read_json_roundtrip(self) -> None:
        path = PATHS.CACHE_FOLDER / "payload.json"
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

    def test_read_json_returns_none_for_invalid_content_in_silent_mode(self) -> None:
        path = PATHS.CACHE_FOLDER / "invalid.json"
        path.write_text("{ invalid json", encoding="utf-8")

        debug(f"Lege absichtlich defektes JSON an: {path}")
        loaded = read_json(path, on_error="silent")
        debug(f"Rueckgabewert fuer defektes JSON: {loaded!r}")

        assert loaded is None