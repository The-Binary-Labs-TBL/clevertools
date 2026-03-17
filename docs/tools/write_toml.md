# `write_toml`

`write_toml()` serializes mapping data to TOML and writes it to disk.

## Signature

```python
write_toml(
    file_path: str | Path,
    data: Mapping[str, Any],
    create_if_missing: bool = True,
    on_error: Literal["raise", "log", "silent"] | None = None,
) -> None
```

## Example

```python
from clevertools import write_toml

write_toml(
    "settings.toml",
    {
        "project": {"name": "clevertools", "version": "0.2.1"},
        "features": {"logging": True, "masking": True},
    },
)
```

## Notes

- `data` must be a mapping like `dict`.
- Parent folders are created automatically when `create_if_missing=True`.