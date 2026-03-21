from __future__ import annotations

from dataclasses import dataclass
from typing import TextIO
import logging
import io
import sys

from ..models import DEFAULT_LOGGER_NAME
from .handlers import reset_handlers
from .logger import get_logger


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
        self.original_stream.write(text)
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
    stdout_original: TextIO | None = None
    stderr_original: TextIO | None = None


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

    if capture_stdout and state.stdout_original is None:
        stdout_stream = sys.stdout
        if stdout_stream is None:
            raise RuntimeError("sys.stdout is not available for capture.")

        state.stdout_original = stdout_stream
        sys.stdout = StreamToLogger(logger, logging.INFO, stdout_stream)

    if capture_stderr and state.stderr_original is None:
        stderr_stream = sys.stderr
        if stderr_stream is None:
            raise RuntimeError("sys.stderr is not available for capture.")

        state.stderr_original = stderr_stream
        sys.stderr = StreamToLogger(logger, logging.ERROR, stderr_stream)

    return logger


def stop_file_logger(name: str = DEFAULT_LOGGER_NAME) -> None:
    state = _BOOTSTRAP_STATE.get(name)
    if state is None:
        return

    if state.stdout_original is not None:
        sys.stdout = state.stdout_original
        state.stdout_original = None

    if state.stderr_original is not None:
        sys.stderr = state.stderr_original
        state.stderr_original = None


def flush_bootstrap_buffer(logger: logging.Logger) -> None:
    state = _BOOTSTRAP_STATE.get(logger.name)
    if state is None:
        return

    for record in state.buffer_handler.drain():
        for handler in logger.handlers:
            if handler is state.buffer_handler:
                continue
            handler.handle(record)


def get_console_stream(name: str = DEFAULT_LOGGER_NAME) -> TextIO | None:
    state = _BOOTSTRAP_STATE.get(name)
    if state is None:
        return None

    if state.stderr_original is not None:
        return state.stderr_original

    return None