# `write_json`

`write_json()` serializes Python data to formatted JSON and writes it to disk.

## Signature

```python
write_json(
    file_path: str | Path,
    data: Any,
    create_if_missing: bool = True,
    ensure_ascii: bool = True,
    indent: int = 4,
    on_error: Literal["raise", "log", "silent"] | None = None,
) -> None
```

## Example: standard JSON output

```python
from clevertools import write_json

write_json(
    "config.json",
    {
        "service": "clevertools",
        "enabled": True,
        "retries": 3,
    },
)
```

## Example: pretty Unicode output

```python
from clevertools import write_json

write_json(
    "build/report.json",
    {"title": "Überblick", "status": "fertig"},
    ensure_ascii=False,
    indent=2,
)
```

## Notes

- `data` must not be `None`.
- With `create_if_missing=True`, parent folders are created automatically.
- Non-serializable objects are rejected through the shared error policy.
- `ensure_ascii=False` is helpful when you want readable Unicode output.