from __future__ import annotations

from collections.abc import Generator
import pytest
import shutil

from .bootstrap import bootstrap
from .paths import PATHS


@pytest.fixture(scope="session", autouse=True)
def clean_cache() -> Generator[None, None, None]:
    bootstrap()

    yield

    if PATHS.CACHE_FOLDER.exists():
        shutil.rmtree(PATHS.CACHE_FOLDER, ignore_errors=True)
        PATHS.CACHE_FOLDER.mkdir(parents=True, exist_ok=True)