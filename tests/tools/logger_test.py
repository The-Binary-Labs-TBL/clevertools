from __future__ import annotations

from clevertools import (
    CleverToolsFormatter,
    configure,
    configure_logger,
    log,
    start_file_logger,
    stop_file_logger
)
from pytest import CaptureFixture
from pathlib import Path
import io
import logging
import sys
import re


DEFAULT_LOG_LINE = "clevertools | [{level}] = {message}"
DATETIME_LOG_PATTERN = (
    r"clevertools \| {level} \| "
    r"\[\d{{4}}-\d{{2}}-\d{{2}}\] \[\d{{2}}:\d{{2}}:\d{{2}}\] = {message}"
)


class LoggerTestBase:
    def _configure_file_logger(
        self,
        *,
        log_path: str | Path,
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


class _TTYStream(io.StringIO):
    def __init__(self, *, isatty: bool) -> None:
        super().__init__()
        self._isatty = isatty

    def isatty(self) -> bool:
        return self._isatty


class TestLoggerFormatting(LoggerTestBase):
    def test_logger_uses_default_format_from_config(self, cache_dir: Path) -> None:
        log_path = cache_dir / "clevertools-default.log"

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

    def test_logger_uses_datetime_format_when_requested(self, cache_dir: Path) -> None:
        log_path = cache_dir / "clevertools-datetime.log"

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

    def test_logger_uses_custom_date_format_for_datetime_preset(self, cache_dir: Path) -> None:
        log_path = cache_dir / "clevertools-custom-date.log"

        self._configure_file_logger(
            log_path=log_path,
            level="INFO",
            format_preset="datetime",
        )

        logger = configure_logger(date_format="%d.%m.%Y", use_colors=False)
        logger.info("hello custom date")

        rendered_line = log_path.read_text(encoding="utf-8").strip()
        assert re.fullmatch(
            r"clevertools \| INFO \| \[\d{2}\.\d{2}\.\d{4}\] \[\d{2}:\d{2}:\d{2}\] = hello custom date",
            rendered_line,
        )

    def test_formatter_uses_handler_stream_for_color_detection(self) -> None:
        formatter = CleverToolsFormatter(
            "[%(levelname)s] %(message)s",
            use_colors=True,
            color_stream=_TTYStream(isatty=True),
        )
        record = logging.LogRecord(
            name="clevertools",
            level=logging.WARNING,
            pathname=__file__,
            lineno=1,
            msg="colored output",
            args=(),
            exc_info=None,
        )

        rendered = formatter.format(record)

        assert "\033[33mWARNING\033[0m" in rendered


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

    def test_logger_respects_custom_format_override_exactly(self, cache_dir: Path) -> None:
        log_path = cache_dir / "clevertools-custom-format.log"

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

    def test_start_file_logger_buffers_early_records_until_final_configuration(self, cache_dir: Path) -> None:
        log_path = cache_dir / "clevertools-bootstrapped.log"

        configure(
            logger_overrides={
                "level": "INFO",
                "console_enabled": False,
                "file_logging_enabled": True,
                "file_log_path": log_path,
            }
        )

        try:
            logger = start_file_logger()
            logger.info("before configure")

            configure_logger(use_colors=False)
            logger.info("after configure")
        finally:
            stop_file_logger()

        rendered_lines = log_path.read_text(encoding="utf-8").splitlines()

        assert len(rendered_lines) == 2
        self._assert_default_line(
            rendered_lines[0],
            level="INFO",
            message="before configure",
        )
        self._assert_default_line(
            rendered_lines[1],
            level="INFO",
            message="after configure",
        )

    def test_start_file_logger_can_capture_stdout_and_stderr(self, cache_dir: Path) -> None:
        log_path = cache_dir / "clevertools-stdio.log"

        configure(
            logger_overrides={
                "level": "INFO",
                "console_enabled": False,
                "file_logging_enabled": True,
                "file_log_path": log_path,
            }
        )

        try:
            start_file_logger(capture_stdout=True, capture_stderr=True)
            print("hello stdout")
            sys.stderr.write("hello stderr\n")
            configure_logger(use_colors=False)
        finally:
            stop_file_logger()

        rendered = log_path.read_text(encoding="utf-8")

        assert "hello stdout" in rendered
        assert "hello stderr" in rendered

    def test_start_file_logger_does_not_duplicate_boot_output_on_console(
        self,
        cache_dir: Path,
        capsys: CaptureFixture[str],
    ) -> None:
        log_path = cache_dir / "clevertools-console-bootstrap.log"

        configure(
            logger_overrides={
                "level": "INFO",
                "console_enabled": True,
                "file_logging_enabled": True,
                "file_log_path": log_path,
            }
        )

        try:
            start_file_logger(capture_stdout=True, capture_stderr=True)
            print("hello stdout")
            sys.stderr.write("hello stderr\n")
            configure_logger(use_colors=False)
        finally:
            stop_file_logger()

        captured = capsys.readouterr()
        rendered_err = [line for line in captured.err.splitlines() if line]

        assert captured.out == ""
        assert rendered_err == [
            DEFAULT_LOG_LINE.format(level="INFO", message="hello stdout"),
            DEFAULT_LOG_LINE.format(level="ERROR", message="hello stderr"),
        ]