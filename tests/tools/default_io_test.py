from __future__ import annotations

from clevertools import read, write
from ..paths import PATHS


class DefaultIOTest:
    def test_write(self) -> None:
        path = PATHS.CACHE_FOLDER / "test_write.txt"
        write(path, "Hello World")
        assert path.exists()
        assert path.read_text(encoding="utf-8") == "Hello World"

    def test_read(self) -> None:
        path = PATHS.CACHE_FOLDER / "test_read.txt"
        path.write_text("Hello World", encoding="utf-8")
        assert read(path) == "Hello World"