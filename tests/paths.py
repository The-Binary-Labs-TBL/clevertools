from __future__ import annotations

from pathlib import Path
import tempfile

class Rout:
    def __init__(self) -> None:
        self.TEMP_FOLDER: Path = Path(tempfile.gettempdir())
        self.CACHE_FOLDER: Path = self.TEMP_FOLDER / "clevertools_cache"

PATHS = Rout()