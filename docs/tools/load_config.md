# `load_config`

`load_config()` reads multiple configuration files, merges overlapping sections, and returns one combined configuration object.

## Signature

```python
load_config(*file_paths: str | Path, on_error: ErrorMode | None = None)
```

## What it does

- Reads each file in the order you pass it in.
- Supports `.toml`, `.json`, `.yaml`, and `.yml`.
- Merges nested tables recursively.
- Combines shared sections such as `pipelines.ai` across multiple files.
- Exposes the merged result through attribute access and dot-path lookups.
- Applies the shared error policy when a file cannot be read or parsed.

## Returns

Returns one merged configuration object.

You can access values like this:

- `config.pipelines.ai.enabled`
- `config.get("pipelines.ai.ai_model")`

## Example

```python
from clevertools import load_config

config = load_config(
    "config/settings.toml",
    "config/content.json",
    "config/content.yaml",
)

print(config.pipelines.ai.enabled)
print(config.pipelines.ai.ai_model)
print(config.get("pipelines.publishing.default_post_status"))
```

## Notes

- Nested mappings are merged recursively across supported file types.
- If the same non-mapping key exists in multiple files, the later file wins.
- Missing files and parse errors follow the shared error policy from the corresponding reader.
- Each loaded document must have a mapping object at its root so it can be merged safely.
- Use `as_dict()` when you need the merged result as a plain dictionary.