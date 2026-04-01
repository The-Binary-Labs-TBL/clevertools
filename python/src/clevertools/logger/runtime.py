from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TextIO
import logging
import io
import sys

from ..models import DEFAULT_LOGGER_NAME, WriteMode
from .handlers import build_file_handler, reset_handlers
from .logger import get_logger
from .options import ResolvedLoggerOptions, resolve_logger_options


class InMemoryLogHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)

    def drain(self) -> list[logging.LogRecord]:
        records = list(self.records)
        self.records.clear()
        return records


class StreamToLogger(io.TextIOBase):
    def __init__(self, logger: logging.Logger, level: int, original_stream: TextIO) -> None:
        self.logger = logger
        self.level = level
        self.original_stream = original_stream
        self._buffer = ""

    def write(self, text: str) -> int:
        self._buffer += text

        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            self._log_line(line)

        return len(text)

    def flush(self) -> None:
        self.original_stream.flush()
        if self._buffer:
            self._log_line(self._buffer)
            self._buffer = ""

    def isatty(self) -> bool:
        return self.original_stream.isatty()

    def _log_line(self, line: str) -> None:
        normalized_line = line.rstrip()
        if normalized_line:
            self.logger.log(self.level, normalized_line)


@dataclass
class BootstrapState:
    buffer_handler: InMemoryLogHandler
    bootstrap_file_handler: logging.Handler | None = None
    bootstrap_file_path: Path | None = None
    stdout_original: TextIO | None = None
    stderr_original: TextIO | None = None
    stdout_redirect: StreamToLogger | None = None
    stderr_redirect: StreamToLogger | None = None


_BOOTSTRAP_STATE: dict[str, BootstrapState] = {}


def start_file_logger(
    *,
    name: str = DEFAULT_LOGGER_NAME,
    level: int | str = "INFO",
    capture_stdout: bool = False,
    capture_stderr: bool = False,
) -> logging.Logger:
    logger = get_logger(name)
    logger.setLevel(level)
    logger.propagate = False

    state = _BOOTSTRAP_STATE.get(name)
    if state is None:
        reset_handlers(logger)
        state = BootstrapState(buffer_handler=InMemoryLogHandler())
        logger.addHandler(state.buffer_handler)
        _BOOTSTRAP_STATE[name] = state
    elif state.buffer_handler not in logger.handlers:
        # Re-enter bootstrap mode cleanly after a previous final configuration.
        reset_handlers(logger)
        logger.addHandler(state.buffer_handler)

    _ensure_bootstrap_file_handler(state, logger=logger, level=level)

    if capture_stdout and state.stdout_original is None:
        stdout_stream = sys.stdout
        if stdout_stream is None:
            raise RuntimeError("sys.stdout is not available for capture.")

        state.stdout_original = stdout_stream
        state.stdout_redirect = StreamToLogger(logger, logging.INFO, stdout_stream)
        sys.stdout = state.stdout_redirect

    if capture_stderr and state.stderr_original is None:
        stderr_stream = sys.stderr
        if stderr_stream is None:
            raise RuntimeError("sys.stderr is not available for capture.")

        state.stderr_original = stderr_stream
        state.stderr_redirect = StreamToLogger(logger, logging.ERROR, stderr_stream)
        sys.stderr = state.stderr_redirect

    return logger


def stop_file_logger(name: str = DEFAULT_LOGGER_NAME) -> None:
    state = _BOOTSTRAP_STATE.get(name)
    if state is None:
        return

    if state.stdout_original is not None:
        if state.stdout_redirect is not None:
            state.stdout_redirect.flush()
        sys.stdout = state.stdout_original
        state.stdout_original = None
        state.stdout_redirect = None

    if state.stderr_original is not None:
        if state.stderr_redirect is not None:
            state.stderr_redirect.flush()
        sys.stderr = state.stderr_original
        state.stderr_original = None
        state.stderr_redirect = None


def flush_bootstrap_buffer(
    logger: logging.Logger,
    *,
    file_write_mode: WriteMode = "runtime",
) -> None:
    state = _BOOTSTRAP_STATE.get(logger.name)
    if state is None:
        return

    bootstrap_file_handler = state.bootstrap_file_handler
    bootstrap_file_path = state.bootstrap_file_path
    final_file_handler = _find_file_handler(logger)

    replay_into_file = True
    if (
        file_write_mode == "buffered"
        and
        bootstrap_file_handler is not None
        and bootstrap_file_path is not None
        and final_file_handler is not None
        and _same_file_target(final_file_handler, bootstrap_file_path)
    ):
        replay_into_file = False

    for record in state.buffer_handler.drain():
        for handler in logger.handlers:
            if handler is state.buffer_handler:
                continue
            if not replay_into_file and handler is final_file_handler:
                continue
            handler.handle(record)

    if bootstrap_file_handler is not None:
        bootstrap_file_handler.close()
        state.bootstrap_file_handler = None
        state.bootstrap_file_path = None


def get_console_stream(name: str = DEFAULT_LOGGER_NAME) -> TextIO | None:
    state = _BOOTSTRAP_STATE.get(name)
    if state is None:
        return None

    if state.stderr_original is not None:
        return state.stderr_original

    return None


def _ensure_bootstrap_file_handler(
    state: BootstrapState,
    *,
    logger: logging.Logger,
    level: int | str,
) -> None:
    options = resolve_logger_options(
        level=level,
        format_preset=None,
        fmt=None,
        date_format=None,
        console_enabled=None,
        file_logging_enabled=None,
        file_log_path=None,
        file_write_mode="buffered",
        use_colors=False,
    )

    if not options.file_logging_enabled or options.file_log_path is None:
        return

    file_path = Path(options.file_log_path)

    if state.bootstrap_file_path == file_path and state.bootstrap_file_handler in logger.handlers:
        return

    if state.bootstrap_file_handler is not None:
        logger.removeHandler(state.bootstrap_file_handler)
        state.bootstrap_file_handler.close()

    bootstrap_file_handler = build_file_handler(_as_bootstrap_file_options(options))
    logger.addHandler(bootstrap_file_handler)
    state.bootstrap_file_handler = bootstrap_file_handler
    state.bootstrap_file_path = file_path


def _as_bootstrap_file_options(options: ResolvedLoggerOptions) -> ResolvedLoggerOptions:
    return ResolvedLoggerOptions(
        level=options.level,
        format_preset=options.format_preset,
        fmt=options.fmt,
        date_format=options.date_format,
        console_enabled=False,
        file_logging_enabled=True,
        file_log_path=options.file_log_path,
        file_write_mode="buffered",
        use_colors=False,
    )


def _find_file_handler(logger: logging.Logger) -> logging.FileHandler | None:
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return handler

    return None


def _same_file_target(handler: logging.FileHandler, expected_path: Path) -> bool:
    return Path(handler.baseFilename) == expected_path.resolve()