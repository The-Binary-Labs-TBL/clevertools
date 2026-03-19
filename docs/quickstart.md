# Quickstart

This example combines configuration, file helpers, masking, and logging.

```python
from clevertools import configure, configure_logger, mask, read_json, write_json

configure(
    error_mode="raise",
    logger_overrides={
        "level": "INFO",
        "console_enabled": True,
    },
)

logger = configure_logger(name="demo", use_colors=False)

payload = {
    "service": "billing",
    "token": mask("sk-demo-123456789", 4, 3),
}

write_json("tmp/config.json", payload)
loaded = read_json("tmp/config.json")

logger.info("Loaded config: %s", loaded)
```

If your configuration is split across multiple TOML, JSON, or YAML files, `load_config()` merges it into one object:

```python
from clevertools import load_config

config = load_config("config/settings.toml", "config/content.yaml")
print(config.pipelines.ai.enabled)
```

Next steps:

- Read [Tools](./tools/README.md) for every public helper.
- Read [Concepts](./concepts/README.md) for shared behavior like error handling and logging.