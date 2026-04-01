# `mask`

`mask()` hides the middle part of a string while keeping a selected number of characters visible at the beginning and end.

It is mainly intended for secrets and identifiers that should still be recognizable in logs without exposing the full value.

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

## Good use cases

- API keys
- access tokens
- customer IDs
- order numbers
- email addresses

## Example: mask a token

```python
from clevertools import mask

print(mask("sk-live-1234567890"))
print(mask("sk-live-1234567890", 3, 4))
```

Typical output:

```text
sk-live-********90
sk-***********7890
```

## Example: mask with a custom character

```python
from clevertools import mask

email = "secret@example.com"
print(mask(email, 2, 11, "#"))
```

Typical output:

```text
se#####example.com
```

## Validation rules

- `value` must be a non-empty string
- `show_start_characters` and `show_end_characters` must be `>= 0`
- `mask_character` must be exactly one character

## Notes

- If validation fails and you are not in `"raise"` mode, the function returns an empty string.
- The helper makes sure at least part of the original value is masked when possible.