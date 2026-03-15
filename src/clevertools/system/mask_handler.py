from __future__ import annotations


def mask(value: str | None, show_start_characters: int | None = None, show_end_characters: int | None = None, *, mask_character: str = "*") -> str:
    """
    Mask a string while keeping part of the beginning or end visible.

    This is useful for values such as API keys, tokens, or passwords that
    should not be shown in full. By default, the function reveals a small
    prefix and suffix, but both visible sections can be adjusted.

    Args:
        value: The value to mask. Returns an empty string when `None`.
        show_start_characters: Number of visible characters at the start.
        show_end_characters: Number of visible characters at the end.
        mask_character: Single character used for the masked middle section.

    Returns:
        The masked string.

    Raises:
        ValueError: If `value` is not a string, if visible counts are negative,
            or if `mask_character` is not exactly one character long.
    """

    if value is None:
        return ""

    if not isinstance(value, str):
        raise ValueError("value must be a string or None")

    default_start = 8
    default_end = 2

    if show_start_characters is not None:
        if show_start_characters < 0:
            raise ValueError("show_start_characters must be >= 0")
        default_start = show_start_characters

    if show_end_characters is not None:
        if show_end_characters < 0:
            raise ValueError("show_end_characters must be >= 0")
        default_end = show_end_characters

    if len(mask_character) != 1:
        raise ValueError("mask_character must be exactly one character")

    if not value:
        return ""

    visible_end_count = min(default_end, max(len(value) - 1, 0))
    remaining_for_start = len(value) - visible_end_count
    visible_start_count = min(default_start, max(remaining_for_start - 1, 0))

    visible_start = value[:visible_start_count]
    visible_end = value[-visible_end_count:] if visible_end_count else ""
    masked_middle_length = len(value) - visible_start_count - visible_end_count
    masked_middle = mask_character * masked_middle_length

    return f"{visible_start}{masked_middle}{visible_end}"
