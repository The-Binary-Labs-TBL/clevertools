# `resolve_logger_options`

`resolve_logger_options()` merges explicit logger arguments with the defaults stored by `configure()`.

## Signature

```python
resolve_logger_options(
    *,
    level: int | str | None,
    format_preset: Literal["default", "datetime"] | None,
    fmt: str | None,
    date_format: str | None,
    console_enabled: bool | None,
    file_logging_enabled: bool | None,
    file_log_path: str | Path | None,
    file_write_mode: Literal["runtime", "buffered"],
    use_colors: bool,
) -> ResolvedLoggerOptions
```

## Example

```python
from clevertools import configure, resolve_logger_options

configure(
    logger_overrides={
        "level": "DEBUG",
        "console_enabled": True,
    }
)

options = resolve_logger_options(
    level=None,
    format_preset="datetime",
    fmt=None,
    date_format=None,
    console_enabled=None,
    file_logging_enabled=False,
    file_log_path=None,
    file_write_mode="runtime",
    use_colors=False,
)

print(options.level)
print(options.format_preset)
```

## Notes

- Explicit function arguments win over stored overrides.
- If `fmt` is omitted, the formatter string comes from `format_preset`.