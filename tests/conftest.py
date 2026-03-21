from __future__ import annotations

from collections.abc import Generator
from pathlib import Path
import pytest
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


from clevertools.configuration import configure, get_config
from clevertools.logger import runtime as logger_runtime
from clevertools.logger.handlers import reset_handlers
from clevertools.models import DEFAULT_LOGGER_NAME
from clevertools.logger.logger import get_logger

@pytest.fixture
def cache_dir(tmp_path: Path) -> Path:
    path = tmp_path / "cache"
    path.mkdir()
    return path


@pytest.fixture(autouse=True)
def reset_clevertools_state() -> Generator[None, None, None]:
    snapshot = get_config()
    logger = get_logger(DEFAULT_LOGGER_NAME)

    logger_runtime.stop_file_logger(DEFAULT_LOGGER_NAME)
    reset_handlers(logger)
    logger_runtime._BOOTSTRAP_STATE.pop(DEFAULT_LOGGER_NAME, None)

    yield

    logger_runtime.stop_file_logger(DEFAULT_LOGGER_NAME)
    reset_handlers(logger)
    logger_runtime._BOOTSTRAP_STATE.pop(DEFAULT_LOGGER_NAME, None)
    configure(
        error_mode=snapshot.error_mode,
        logger_overrides=dict(snapshot.logger_overrides),
    )