from __future__ import annotations

import pytest

from clevertools.file.default_io import read, write

from ..paths import PATHS
from ._debug import debug


class TestDefaultIO:
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

    def test_read_supports_string_paths(self) -> None:
        path = PATHS.CACHE_FOLDER / "test_read_from_str.txt"
        path.write_text("Hello From String Path", encoding="utf-8")

        assert read(str(path), on_error="raise") == "Hello From String Path"

    def test_write_and_read_bytes(self) -> None:
        path = PATHS.CACHE_FOLDER / "test_bytes.bin"
        payload = b"\x00\x01hello\xff"

        write(path, payload, on_error="raise")

        assert path.exists()
        assert path.read_bytes() == payload
        assert read(path, mode="bytes", on_error="raise") == payload

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

    def test_read_directory_path_raises_is_a_directory_error(self) -> None:
        with pytest.raises(IsADirectoryError, match="Path is not a file"):
            read(PATHS.CACHE_FOLDER, on_error="raise")

    def test_read_rejects_unsupported_mode(self) -> None:
        path = PATHS.CACHE_FOLDER / "unsupported_mode.txt"
        path.write_text("Hello World", encoding="utf-8")

        with pytest.raises(ValueError, match="Unsupported read mode"):
            read(path, mode="json", on_error="raise")

    def test_write_rejects_non_string_input(self) -> None:
        path = PATHS.CACHE_FOLDER / "invalid_write.txt"

        with pytest.raises(TypeError, match="Text data must be a string"):
            write(path, 123, on_error="raise")

    def test_write_raises_when_target_is_directory(self) -> None:
        with pytest.raises(IsADirectoryError, match="Path is not a file"):
            write(PATHS.CACHE_FOLDER, "Hello Directory", create_if_missing=False, on_error="raise")