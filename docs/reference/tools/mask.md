# `mask`

`mask()` hides sensitive text while keeping a configurable part of the value
visible.

## Signature

```python
mask(
    value,
    show_start_characters=None,
    show_end_characters=None,
    *,
    mask_character="*",
)
```

## Behavior

- returns `""` when `value` is `None`
- keeps 8 characters at the start and 2 at the end by default
- allows custom visible prefix and suffix lengths
- validates invalid arguments with `ValueError`

## Example

```python
from clevertools import mask

masked = mask("sk-live-1234567890", 3, 4)
```