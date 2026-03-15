from __future__ import annotations

from .paths import PATHS

def bootstrap() -> None:
    try:
        if not PATHS.CACHE_FOLDER.exists():
            PATHS.CACHE_FOLDER.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        raise Exception(f"Failed to run bootstrap: {exc}")