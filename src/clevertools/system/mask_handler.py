from __future__ import annotations

from typing import Optional

def mask(value: str, show_start_characters: Optional[int] = None, show_end_characters: Optional[int] = None) -> str:
    if value is None:
        return ""

    start: int = 8
    end: int = 2

    if show_start_characters is not None:
        if show_start_characters < 0:
            raise ValueError("show_start_characters must be more than 0!")
        if show_start_characters > 0:
            start = show_start_characters

    if show_end_characters is not None:
        if show_end_characters < 0:
            raise ValueError("show_end_characters must be more than 0!")
        if show_end_characters > 0:
            end = show_end_characters

    try:
        visible_start = value[: start]
        visible_end = value[-end:]
        masked_middle = "*" * (len(value) - start - end)

        return f"{visible_start}{masked_middle}{visible_end}"
    except ValueError as exc:
        raise ValueError(f"Failed to mask: {exc}") from exc