# `write`

`write()` writes plain text or raw bytes to a file.

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

## Example: write a text file

```python
from clevertools import write

write("notes.txt", "Hello from clevertools")
```

## Example: write binary data

```python
from clevertools import write

write("cache/blob.bin", b"\x00\x01hello\xff")
```

## Example: require an existing target

```python
from clevertools import write

write("existing/output.txt", "updated content", create_if_missing=False, on_error="raise")
```

## Notes

- With `create_if_missing=False`, the file must already exist and must be a normal file.
- Non-`str` and non-`bytes` payloads are rejected.
- The function does not return the written content; it either succeeds or follows the shared error policy.