from __future__ import annotations

from clevertools import read, write

from ..paths import PATHS
from ._debug import debug


class DefaultIOTest:
    def test_write(self) -> None:
        path = PATHS.CACHE_FOLDER / "test_write.txt"
        debug(f"Schreibe Textdatei nach: {path}")
        write(path, "Hello World")
        debug(f"Dateiinhalt nach write(...): {path.read_text(encoding='utf-8')}")
        assert path.exists()
        assert path.read_text(encoding="utf-8") == "Hello World"

    def test_read(self) -> None:
        path = PATHS.CACHE_FOLDER / "test_read.txt"
        path.write_text("Hello World", encoding="utf-8")
        debug(f"Lese vorbereitete Datei: {path}")
        assert read(path) == "Hello World"

    def test_write_does_not_create_file_when_creation_is_disabled(self) -> None:
        path = PATHS.CACHE_FOLDER / "write_disabled.txt"
        if path.exists():
            path.unlink()

        debug(f"Versuche in nicht existierende Datei zu schreiben: {path}")
        write(path, "Hello Blocked World", create_if_missing=False, on_error="silent")
        debug(f"Datei existiert nach blockiertem Write: {path.exists()}")

        assert not path.exists()

    def test_read_missing_file_returns_none_in_silent_mode(self) -> None:
        path = PATHS.CACHE_FOLDER / "missing_read.txt"
        if path.exists():
            path.unlink()

        debug(f"Lese absichtlich fehlende Datei: {path}")
        content = read(path, on_error="silent")
        debug(f"Rueckgabewert fuer fehlende Datei: {content!r}")

        assert content is None