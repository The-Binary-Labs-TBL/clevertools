from __future__ import annotations

from typing import Dict
import logging
import sys

from ..models import DEFAULT_COLORS, DEFAULT_DATE_FORMAT, DEFAULT_TIME_FORMAT, RESET

class CleverToolsFormatter(logging.Formatter):
    def __init__(self, fmt: str, datefmt: str | None = None, *, use_colors: bool = False) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        original_values = self._remember_record_state(record)

        self._set_structured_timestamp_fields(record)
        self._set_colored_level_name(record)

        try:
            return super().format(record)
        finally:
            self._restore_record_state(record, original_values)

    def _remember_record_state( self, record: logging.LogRecord) -> Dict[str, str | None]:
        return {
            "levelname": record.levelname,
            "date": getattr(record, "date", None),
            "time": getattr(record, "time", None),
        }

    def _set_structured_timestamp_fields(self, record: logging.LogRecord) -> None:
        record.date = self.formatTime(record, DEFAULT_DATE_FORMAT)
        record.time = self.formatTime(record, DEFAULT_TIME_FORMAT)

    def _set_colored_level_name(self, record: logging.LogRecord) -> None:
        if not self.use_colors or not sys.stdout.isatty():
            return

        color = DEFAULT_COLORS.get(record.levelname)
        if color is None:
            return

        record.levelname = f"{color}{record.levelname}{RESET}"

    def _restore_record_state(self, record: logging.LogRecord, original_values: Dict[str, str | None]) -> None:
        record.levelname = original_values["levelname"] or record.levelname

        self._restore_optional_field(record, "date", original_values["date"])
        self._restore_optional_field(record, "time", original_values["time"])

    def _restore_optional_field(
        self,
        record: logging.LogRecord,
        field_name: str,
        original_value: str | None,
    ) -> None:
        if original_value is None:
            delattr(record, field_name)
            return

        setattr(record, field_name, original_value)