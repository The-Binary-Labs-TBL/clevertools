# Concepts

These pages explain the shared rules behind multiple helpers. They are especially useful when you want to understand package-wide behavior instead of one individual function.

## Pages in this section

- [Error Handling](./error-handling.md) explains `on_error`, fallback values, and package-wide defaults from `configure()`.
- [Logging](./logging.md) explains presets, write modes, bootstrap logging, and how the logging helpers fit together.

## When to read this section

Read these pages when you want to know:

- why some helpers return `None`, `""`, or simply do nothing on failure
- how `error_mode="raise"`, `"log"`, and `"silent"` differ
- how logger overrides from `configure()` affect `configure_logger()`
- when to use `start_file_logger()` before the final logging setup exists