# Tools

This section is the full public API map for `clevertools`. Each page explains one helper in detail, including what it does, when to use it, and examples you can adapt directly.

## Read this page like a toolbox

If you know your goal already, start here:

- I want package-wide defaults: [configure](./configure.md)
- I want to hide a secret before logging it: [mask](./mask.md)
- I want to read or write files: [read](./read.md), [write](./write.md)
- I want JSON, TOML, or YAML helpers: [read_json](./read_json.md), [write_json](./write_json.md), [read_toml](./read_toml.md), [write_toml](./write_toml.md), [read_yaml](./read_yaml.md), [write_yaml](./write_yaml.md)
- I want to merge config files: [load_config](./load_config.md)
- I want a logger quickly: [configure_logger](./configure_logger.md)
- I need early startup logging: [start_file_logger](./start_file_logger.md), [stop_file_logger](./stop_file_logger.md)
- I need lower-level logging control: [get_logger](./get_logger.md), [CleverToolsFormatter](./clevertools_formatter.md), [build_console_handler](./build_console_handler.md), [build_file_handler](./build_file_handler.md), [reset_handlers](./reset_handlers.md), [resolve_logger_options](./resolve_logger_options.md)

## Core helpers

- [configure](./configure.md)
  Stores global defaults such as `error_mode` and logger overrides.
- [log](./log.md)
  The shared default logger instance for small scripts and default package logging.
- [mask](./mask.md)
  Masks the middle of sensitive strings while keeping part of the start and end visible.

## File helpers

- [read](./read.md)
  Reads plain text or raw bytes from a file.
- [write](./write.md)
  Writes plain text or raw bytes to a file.
- [read_json](./read_json.md)
  Reads and parses JSON into Python objects.
- [write_json](./write_json.md)
  Writes Python objects as formatted JSON.
- [read_toml](./read_toml.md)
  Reads TOML into a dictionary.
- [write_toml](./write_toml.md)
  Writes mapping data as TOML.
- [read_yaml](./read_yaml.md)
  Reads YAML into Python objects.
- [write_yaml](./write_yaml.md)
  Writes Python objects as YAML.
- [load_config](./load_config.md)
  Merges multiple TOML, JSON, and YAML config files into one object with attribute and dot-path access.

## Logging helpers

- [configure_logger](./configure_logger.md)
  High-level logger setup for console and file logging.
- [start_file_logger](./start_file_logger.md)
  Starts bootstrap logging before your final logger setup exists.
- [stop_file_logger](./stop_file_logger.md)
  Restores captured streams after bootstrap logging.
- [get_logger](./get_logger.md)
  Returns a named logger without changing its handlers.
- [CleverToolsFormatter](./clevertools_formatter.md)
  Custom formatter with `date`, `time`, and optional color support.
- [build_console_handler](./build_console_handler.md)
  Creates a stream handler from resolved options.
- [build_file_handler](./build_file_handler.md)
  Creates a file handler from resolved options.
- [reset_handlers](./reset_handlers.md)
  Removes and closes all handlers on a logger.
- [resolve_logger_options](./resolve_logger_options.md)
  Merges explicit logger arguments with defaults from `configure()`.

## Suggested reading order

For most users, this order works well:

1. [configure](./configure.md)
2. [read](./read.md) and [write](./write.md)
3. [read_json](./read_json.md), [write_json](./write_json.md), [read_toml](./read_toml.md), [write_toml](./write_toml.md), [read_yaml](./read_yaml.md), [write_yaml](./write_yaml.md)
4. [load_config](./load_config.md)
5. [configure_logger](./configure_logger.md)
6. the lower-level logging pages only if you need more control