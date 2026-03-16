from __future__ import annotations

from pytest import CaptureFixture
import re

from clevertools import configure, configure_logger, log
from ..paths import PATHS


class TestLogger:
    def test_logger_uses_default_default_format_from_config(self) -> None:
        log_path = PATHS.CACHE_FOLDER / "clevertools-default.log"

        configure(
            logger_overrides={
                "level": "DEBUG",
                "console_enabled": False,
                "file_logging_enabled": True,
                "file_log_path": log_path,
            }
        )

        logger = configure_logger()
        logger.debug("hello logger")

        assert log_path.exists()
        assert logger is log
        assert (
            log_path.read_text(encoding="utf-8").strip()
            == "clevertools | [DEBUG] hello logger"
        )

    def test_logger_uses_datetime_default_format_when_requested(self) -> None:
        log_path = PATHS.CACHE_FOLDER / "clevertools-datetime.log"

        configure(
            logger_overrides={
                "level": "INFO",
                "format_preset": "datetime",
                "console_enabled": False,
                "file_logging_enabled": True,
                "file_log_path": log_path,
            }
        )

        logger = configure_logger()
        logger.info("hello datetime")

        assert log_path.exists()
        assert re.fullmatch(
            r"clevertools \| INFO \| \[\d{4}-\d{2}-\d{2}\] \[\d{2}:\d{2}:\d{2}\] hello datetime",
            log_path.read_text(encoding="utf-8").strip(),
        )

    def test_logger_writes_default_format_to_console(self, capsys: CaptureFixture[str]) -> None:
        configure(
            logger_overrides={
                "level": "INFO",
                "console_enabled": True,
                "file_logging_enabled": False,
            }
        )

        logger = configure_logger(use_colors=False)
        logger.info("hello console")

        captured = capsys.readouterr()

        assert captured.out == ""
        assert captured.err.strip() == "clevertools | [INFO] hello console"

    def test_logger_writes_datetime_format_to_console(self, capsys: CaptureFixture[str]) -> None:
        configure(
            logger_overrides={
                "level": "INFO",
                "format_preset": "datetime",
                "console_enabled": True,
                "file_logging_enabled": False,
            }
        )

        logger = configure_logger(use_colors=False)
        logger.info("hello console datetime")

        captured = capsys.readouterr()

        assert captured.out == ""
        assert re.fullmatch(
            r"clevertools \| INFO \| \[\d{4}-\d{2}-\d{2}\] \[\d{2}:\d{2}:\d{2}\] hello console datetime",
            captured.err.strip(),
        )