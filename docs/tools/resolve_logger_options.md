# `resolve_logger_options`

`resolve_logger_options()` merges explicit logger arguments with any defaults stored by `configure()`. The result is a resolved options object used internally by `configure_logger()`.

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

## Example: inspect the final logger settings

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
print(options.console_enabled)
```

## Notes

- Explicit function arguments win over stored overrides.
- If `fmt` is omitted, the formatter string is derived from `format_preset`.
- This helper is mainly useful when you want visibility into the exact logger settings before building handlers manually.