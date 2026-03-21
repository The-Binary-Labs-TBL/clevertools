from __future__ import annotations

from clevertools.system.config_handler import load_config
from pathlib import Path
import pytest
import json


pytest.importorskip("yaml")


from ._debug import debug

def test_load_config_merges_multiple_toml_files_and_supports_attribute_access(cache_dir: Path) -> None:
    settings_path = cache_dir / "settings.config_handler.toml"
    content_path = cache_dir / "content.config_handler.toml"

    debug(f"Schreibe Settings-Datei nach {settings_path}")
    settings_path.write_text(
        """
[program]
debug = false

[pipelines.ai]
enabled = true
cleanup_temp = true

[pipelines.publishing]
enabled = false
""".strip()
        + "\n",
        encoding="utf-8",
    )

    debug(f"Schreibe Content-Datei nach {content_path}")
    content_path.write_text(
        """
[pipelines.ai]
ai_model = "gpt-oss:20B"
valid_local_ai_models = ["gpt-oss:20B", "mistral-small3.1:24b"]

[pipelines.publishing]
default_post_status = "draft"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    config = load_config(settings_path, content_path)
    debug(f"Zusammengefuehrte Config: {config.as_dict()}")

    assert config.program.debug is False
    assert config.pipelines.ai.enabled is True
    assert config.pipelines.ai.cleanup_temp is True
    assert config.pipelines.ai.ai_model == "gpt-oss:20B"
    assert config.pipelines.ai.valid_local_ai_models == ["gpt-oss:20B", "mistral-small3.1:24b"]
    assert config.pipelines.publishing.enabled is False
    assert config.pipelines.publishing.default_post_status == "draft"
    assert config.get("pipelines.ai.enabled") is True
    assert config.get("pipelines.ai.ai_model") == "gpt-oss:20B"
    assert config.get("pipelines.missing.value", "fallback") == "fallback"

def test_load_config_merges_toml_json_and_yaml_in_order(cache_dir: Path) -> None:
    settings_path = cache_dir / "settings.mixed.config_handler.toml"
    content_path = cache_dir / "content.mixed.config_handler.json"
    overrides_path = cache_dir / "overrides.mixed.config_handler.yaml"

    settings_path.write_text(
        """
[program]
debug = false

[pipelines.ai]
enabled = true
model = "local-default"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    content_path.write_text(
        json.dumps(
            {
                "pipelines": {
                    "ai": {
                        "model": "gpt-oss:20B",
                        "cleanup_temp": True,
                    }
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    overrides_path.write_text(
        """
pipelines:
  ai:
    cleanup_temp: false
  publishing:
    default_post_status: draft
""".strip()
        + "\n",
        encoding="utf-8",
    )

    config = load_config(settings_path, content_path, overrides_path, on_error="raise")

    assert config.program.debug is False
    assert config.pipelines.ai.enabled is True
    assert config.pipelines.ai.model == "gpt-oss:20B"
    assert config.pipelines.ai.cleanup_temp is False
    assert config.pipelines.publishing.default_post_status == "draft"

def test_load_config_rejects_non_mapping_root_in_json(cache_dir: Path) -> None:
    path = cache_dir / "invalid_root.config_handler.json"
    path.write_text("[1, 2, 3]\n", encoding="utf-8")

    with pytest.raises(TypeError, match="Config root must be a mapping"):
        load_config(path, on_error="raise")