# `write_yaml`

`write_yaml()` serializes a Python value to YAML and writes it to disk.

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

## Example

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

## Notes

- `data` must not be `None`.
- With `create_if_missing=True`, parent folders are created automatically.
- Serialization errors are handled through the shared error policy.