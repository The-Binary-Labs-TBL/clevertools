from __future__ import annotations

from collections.abc import Generator
from pathlib import Path
import sys
import pytest
import shutil

from .bootstrap import bootstrap
from .paths import PATHS

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture(scope="session", autouse=True)
def clean_cache() -> Generator[None, None, None]:
    bootstrap()

    yield

    if PATHS.CACHE_FOLDER.exists():
        shutil.rmtree(PATHS.CACHE_FOLDER, ignore_errors=True)
        PATHS.CACHE_FOLDER.mkdir(parents=True, exist_ok=True)