# `write`

`write()` stores text or bytes in a file.

## Signature

```python
write(
    file_path: str | Path,
    data: str | bytes,
    create_if_missing: bool = True,
    on_error: Literal["raise", "log", "silent"] | None = None,
) -> None
```

## Behavior

- `str` data is written as UTF-8 text
- `bytes` data is written unchanged
- parent folders are created automatically when `create_if_missing=True`

## Example

```python
from clevertools import write

write("notes.txt", "Hello from clevertools")
write("cache/blob.bin", b"\x00\x01hello\xff")
```

## Notes

- With `create_if_missing=False`, the target file must already exist.
- Non-`str` and non-`bytes` payloads are rejected.