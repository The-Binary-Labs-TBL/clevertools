# `read`

`read()` loads a file as UTF-8 text or raw bytes.

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

## Example

```python
from clevertools import read

text = read("notes.txt")
payload = read("image.bin", mode="bytes")
```

## Notes

- Missing files return `None` unless the active error mode raises.
- Directories are rejected with `IsADirectoryError`.
- Unsupported modes raise `ValueError` in `"raise"` mode.