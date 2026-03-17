# `mask`

`mask()` hides the middle of a string while keeping a configurable prefix and suffix visible.

## Signature

```python
mask(
    value: str,
    show_start_characters: int | None = None,
    show_end_characters: int | None = None,
    mask_character: str = "*",
    on_error: Literal["raise", "log", "silent"] | None = None,
) -> str
```

## Defaults

- visible prefix: `8` characters
- visible suffix: `2` characters
- mask character: `*`

## Example

```python
from clevertools import mask

print(mask("sk-live-1234567890"))
print(mask("sk-live-1234567890", 3, 4))
print(mask("secret@example.com", 2, 11, "#"))
```

## Typical output

```text
sk-live-********90
sk-***********7890
se#####example.com
```

## Validation rules

- `value` must be a non-empty string.
- `show_start_characters` and `show_end_characters` must be `>= 0`.
- `mask_character` must be exactly one character.