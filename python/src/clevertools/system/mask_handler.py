from __future__ import annotations

from typing import Optional

from ..errors.policy import handle_error
from ..configuration import ErrorMode

def mask(
    value: str,
    show_start_characters: Optional[int] = None,
    show_end_characters: Optional[int] = None,
    mask_character: str = "*",
    on_error: Optional[ErrorMode] = None
) -> str:
    """
    Mask the middle portion of a string while keeping selected characters at
    the beginning and end visible.

    This helper is useful for obfuscating sensitive values such as API keys,
    tokens, IDs, or personal data before logging or displaying them.

    Args:
        value: Input string that should be partially masked.
        show_start_characters: Number of characters to keep visible at the
            beginning of the string. If not provided, `8` characters are shown
            by default.
        show_end_characters: Number of characters to keep visible at the end
            of the string. If not provided, `2` characters are shown by
            default.
        mask_character: Single character used to replace the masked portion of
            the string.
        on_error: Error handling mode. Use `"raise"` to re-raise the exception,
            `"log"` to log the error and return an empty string, or `"silent"`
            to return an empty string without logging.

    Returns:
        The masked string, or an empty string when validation fails and the
        selected error mode does not raise.
    """

    if not isinstance(value, str):
        return handle_error(ValueError("value must be a string"), on_error=on_error, fallback="")

    default_start = 8
    default_end = 2

    if show_start_characters is not None:
        if show_start_characters < 0:
            return handle_error(ValueError("show_start_characters must be >= 0"), on_error=on_error, fallback="")
        default_start = show_start_characters

    if show_end_characters is not None:
        if show_end_characters < 0:
            return handle_error(ValueError("show_end_characters must be >= 0"), on_error=on_error, fallback="")
        default_end = show_end_characters

    if len(mask_character) != 1:
        return handle_error(ValueError("mask_character must be exactly one character"), on_error=on_error, fallback="")

    if not value:
        return handle_error(ValueError("to use mask you need to set the value"), on_error=on_error, fallback="")

    try:
        vis_end: int = min(default_end, max(len(value) - 1, 0))
        vis_start: int = min(default_start, max(len(value) - vis_end - 1, 0))

        length: int = len(value) - vis_start - vis_end
        
        visible_start: str = value[: vis_start]
        masked_middle: str = mask_character * length
        visible_end: str = value[-vis_end:] if vis_end > 0 else ""

        return f"{visible_start}{masked_middle}{visible_end}"
    except Exception as exc:
        return handle_error(exc, on_error=on_error, fallback="")