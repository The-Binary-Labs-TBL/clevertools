# `read`

`read()` loads a file either as UTF-8 text or as raw bytes.

## Signature

```python
read(
    file_path: str | Path,
    mode: Literal["str", "bytes"] = "str",
    on_error: Literal["raise", "log", "silent"] | None = None,
) -> str | bytes | None
```

## Modes

- `"str"` returns UTF-8 decoded text
- `"bytes"` returns raw file bytes

## Example: read a text file

```python
from clevertools import read

text = read("notes.txt", on_error="raise")
print(text)
```

## Example: read binary data

```python
from clevertools import read

payload = read("cache/blob.bin", mode="bytes")
if payload is not None:
    print(len(payload))
```

## Notes

- Missing files return `None` unless the selected error mode raises.
- Directory paths are rejected.
- Text mode always expects UTF-8.
- Unsupported `mode` values trigger the shared error policy.