from __future__ import annotations

from clevertools import configure, configure_logger
from ..paths import PATHS


class TestLogger:
    def test_logger_uses_defaults_from_config(self) -> None:
        log_path = PATHS.CACHE_FOLDER / "clevertools.log"

        configure(
            logger_overrides={
                "level": "DEBUG",
                "fmt": "%(levelname)s:%(message)s",
                "console_enabled": False,
                "file_logging_enabled": True,
                "file_log_path": log_path,
            }
        )

        logger = configure_logger()
        logger.debug("hello logger")

        assert log_path.exists()
        assert log_path.read_text(encoding="utf-8").strip() == "DEBUG:hello logger"