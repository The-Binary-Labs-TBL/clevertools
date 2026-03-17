from __future__ import annotations

import re

from pytest import CaptureFixture

from clevertools import configure, configure_logger, log

from ..paths import PATHS

DEFAULT_LOG_LINE = "clevertools | [{level}] = {message}"
DATETIME_LOG_PATTERN = (
    r"clevertools \| {level} \| "
    r"\[\d{{4}}-\d{{2}}-\d{{2}}\] \[\d{{2}}:\d{{2}}:\d{{2}}\] = {message}"
)


class LoggerTestBase:
    def _configure_file_logger(
        self,
        *,
        log_path: str,
        level: str,
        format_preset: str = "default",
    ) -> None:
        configure(
            logger_overrides={
                "level": level,
                "format_preset": format_preset,
                "console_enabled": False,
                "file_logging_enabled": True,
                "file_log_path": log_path,
            }
        )

    def _configure_console_logger(self, *, level: str, format_preset: str = "default") -> None:
        configure(
            logger_overrides={
                "level": level,
                "format_preset": format_preset,
                "console_enabled": True,
                "file_logging_enabled": False,
            }
        )

    def _assert_default_line(self, rendered_line: str, *, level: str, message: str) -> None:
        assert rendered_line == DEFAULT_LOG_LINE.format(level=level, message=message)

    def _assert_datetime_line(self, rendered_line: str, *, level: str, message: str) -> None:
        pattern = DATETIME_LOG_PATTERN.format(level=level, message=re.escape(message))
        assert re.fullmatch(pattern, rendered_line)


class TestLoggerFormatting(LoggerTestBase):
    def test_logger_uses_default_format_from_config(self) -> None:
        log_path = PATHS.CACHE_FOLDER / "clevertools-default.log"

        self._configure_file_logger(log_path=log_path, level="DEBUG")

        logger = configure_logger()
        logger.debug("hello logger")

        assert log_path.exists()
        assert logger is log
        self._assert_default_line(
            log_path.read_text(encoding="utf-8").strip(),
            level="DEBUG",
            message="hello logger",
        )

    def test_logger_uses_datetime_format_when_requested(self) -> None:
        log_path = PATHS.CACHE_FOLDER / "clevertools-datetime.log"

        self._configure_file_logger(
            log_path=log_path,
            level="INFO",
            format_preset="datetime",
        )

        logger = configure_logger()
        logger.info("hello datetime")

        assert log_path.exists()
        self._assert_datetime_line(
            log_path.read_text(encoding="utf-8").strip(),
            level="INFO",
            message="hello datetime",
        )

    def test_logger_writes_default_format_to_console(self, capsys: CaptureFixture[str]) -> None:
        self._configure_console_logger(level="INFO")

        logger = configure_logger(use_colors=False)
        logger.info("hello console")

        captured = capsys.readouterr()

        assert captured.out == ""
        self._assert_default_line(
            captured.err.strip(),
            level="INFO",
            message="hello console",
        )

    def test_logger_writes_datetime_format_to_console(self, capsys: CaptureFixture[str]) -> None:
        self._configure_console_logger(level="INFO", format_preset="datetime")

        logger = configure_logger(use_colors=False)
        logger.info("hello console datetime")

        captured = capsys.readouterr()

        assert captured.out == ""
        self._assert_datetime_line(
            captured.err.strip(),
            level="INFO",
            message="hello console datetime",
        )


class TestLoggerHardening(LoggerTestBase):
    def test_logger_does_not_duplicate_console_output_after_reconfiguration(
        self,
        capsys: CaptureFixture[str],
    ) -> None:
        self._configure_console_logger(level="INFO")

        first_logger = configure_logger(use_colors=False)
        second_logger = configure_logger(use_colors=False)
        second_logger.info("single console line")

        captured = capsys.readouterr()
        rendered_lines = [line for line in captured.err.splitlines() if line]

        assert first_logger is second_logger
        assert len(rendered_lines) == 1
        self._assert_default_line(
            rendered_lines[0],
            level="INFO",
            message="single console line",
        )

    def test_logger_respects_custom_format_override_exactly(self) -> None:
        log_path = PATHS.CACHE_FOLDER / "clevertools-custom-format.log"

        configure(
            logger_overrides={
                "level": "WARNING",
                "fmt": "[%(levelname)s] %(message)s",
                "console_enabled": False,
                "file_logging_enabled": True,
                "file_log_path": log_path,
            }
        )

        logger = configure_logger()
        logger.warning("custom override")

        assert log_path.exists()
        assert log_path.read_text(encoding="utf-8").strip() == "[WARNING] custom override"