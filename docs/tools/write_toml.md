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

## Example: write a settings file

```python
from clevertools import write_toml

write_toml(
    "settings.toml",
    {
        "project": {"name": "clevertools", "version": "1.4.1"},
        "features": {"logging": True, "masking": True},
    },
)
```

## Example: export generated config

```python
from clevertools import write_toml

generated = {
    "build": {"target": "prod"},
    "paths": {"cache": ".cache"},
}

write_toml("build/generated.toml", generated)
```

## Notes

- `data` must be a mapping such as `dict`.
- Parent folders are created automatically when `create_if_missing=True`.
- Serialization relies on `tomli_w`, so that dependency must be installed.