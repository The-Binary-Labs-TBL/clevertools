# `write_yaml`

`write_yaml()` serializes Python data to YAML and writes it to disk.

## Signature

```python
write_yaml(
    file_path: str | Path,
    data: Any,
    create_if_missing: bool = True,
    allow_unicode: bool = True,
    sort_keys: bool = False,
    on_error: Literal["raise", "log", "silent"] | None = None,
) -> None
```

## Example: write a readable YAML config

```python
from clevertools import write_yaml

write_yaml(
    "config.yaml",
    {
        "service": "clevertools",
        "enabled": True,
        "labels": ["yaml", "config"],
    },
    allow_unicode=True,
    sort_keys=False,
)
```

## Example: preserve non-ASCII text

```python
from clevertools import write_yaml

write_yaml(
    "content/meta.yaml",
    {"title": "Überblick", "language": "de"},
    allow_unicode=True,
)
```

## Notes

- `data` must not be `None`.
- With `create_if_missing=True`, parent folders are created automatically.
- `sort_keys=False` is useful when output order should stay close to your input structure.