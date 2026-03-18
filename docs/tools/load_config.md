# `load_config`

`load_config()` reads multiple TOML files, merges overlapping sections, and returns one combined configuration object.

## Signature

```python
load_config(*file_paths: str | Path)
```

## What it does

- Reads each TOML file in the order you pass it in.
- Merges nested tables recursively.
- Combines shared sections such as `pipelines.ai` across multiple files.
- Exposes the merged result through attribute access and dot-path lookups.

## Returns

Returns one merged configuration object.

You can access values like this:

- `config.pipelines.ai.enabled`
- `config.get("pipelines.ai.ai_model")`

## Example

```python
from clevertools import load_config

config = load_config("config/settings.toml", "config/content.toml")

print(config.pipelines.ai.enabled)
print(config.pipelines.ai.ai_model)
print(config.get("pipelines.publishing.default_post_status"))
```

## Notes

- Nested TOML tables are merged recursively.
- If the same non-table key exists in multiple files, the later file wins.
- Missing files and TOML parse errors follow the shared error policy from `read_toml()`.
- Use `as_dict()` when you need the merged result as a plain dictionary.