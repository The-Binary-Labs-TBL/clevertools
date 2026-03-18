from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping
from faker import Faker

from clevertools import configure, log, read_json, read_toml, write_json, write_toml
from ..paths import PATHS


def _deep_merge(base: dict[str, Any], incoming: Mapping[str, Any]) -> dict[str, Any]:
    for key, value in incoming.items():
        current = base.get(key)

        if isinstance(current, dict) and isinstance(value, Mapping):
            base[key] = _deep_merge(dict(current), value)
            continue

        if isinstance(value, Mapping):
            base[key] = _deep_merge({}, value)
            continue

        base[key] = value

    return base


class ConfigView:
    def __init__(self, data: Mapping[str, Any]) -> None:
        self._data = dict(data)

    def __getattr__(self, name: str) -> Any:
        try:
            value = self._data[name]
        except KeyError as exc:
            raise AttributeError(f"Config key not found: {name}") from exc
        return self._wrap(value)

    def get(self, path: str, default: Any = None) -> Any:
        current: Any = self

        for part in path.split("."):
            if not part:
                return default

            if isinstance(current, ConfigView):
                if part not in current._data:
                    return default
                current = current._data[part]
                current = self._wrap(current)
                continue

            if isinstance(current, Mapping):
                if part not in current:
                    return default
                current = current[part]
                continue

            return default

        return current

    @staticmethod
    def _wrap(value: Any) -> Any:
        if isinstance(value, Mapping):
            return ConfigView(value)
        return value


def load_config_files(*file_paths: Path | str) -> ConfigView:
    merged: dict[str, Any] = {}

    for file_path in file_paths:
        loaded = read_toml(file_path, on_error="raise")
        if loaded is None:
            continue
        merged = _deep_merge(merged, loaded)

    return ConfigView(merged)


class StaticTestRunner:
    def __init__(self) -> None:
        self.fake = Faker("de_DE")
        self.tmp_settings_toml: Path = PATHS.CACHE_FOLDER / "settings.toml"
        self.tmp_content_toml: Path = PATHS.CACHE_FOLDER / "content.toml"
        self.tmp_json: Path = PATHS.CACHE_FOLDER / "users.json"

    def configure_logger(self) -> None:
        configure(
            error_mode="log",
            logger_overrides={
                "name": "ClevertoolsStaticTest",
                "level": "INFO",
                "format_preset": "datetime",
                "file_logging_enabled": True,
                "file_log_path": PATHS.CACHE_FOLDER / "clevertools_static_test.log",
                "use_colors": True
            },
        )
        log.info("Logger configured for static IO test run.")

    def build_settings_payload(self) -> dict[str, Any]:
        log.info("Building settings TOML payload for configuration test data.")
        payload = {
            "program": {
                "enviroment": "release",
                "wait_for_enter": True,
            },
            "logger": {
                "name": "ClevertoolsStaticTest",
                "level": "INFO",
                "format_preset": "datetime",
                "file_logging_enabled": True,
                "file_log_path": str(PATHS.CACHE_FOLDER / "clevertools_static_test.log"),
            },
            "pipelines": {
                "ai": {
                    "enabled": True,
                    "cleanup_temp": True,
                }
            },
        }
        log.info("Settings TOML payload prepared successfully.")
        return payload

    def build_content_payload(self) -> dict[str, Any]:
        log.info("Building content TOML payload for configuration merge test.")
        payload = {
            "program": {
                "paths": [
                    str(PATHS.CACHE_FOLDER / "hello"),
                    str(PATHS.CACHE_FOLDER / "world"),
                    str(PATHS.CACHE_FOLDER / "my"),
                    str(PATHS.CACHE_FOLDER / "name"),
                    str(PATHS.CACHE_FOLDER / "is"),
                    str(PATHS.CACHE_FOLDER / "b7binw13"),
                    str(PATHS.CACHE_FOLDER / "yayxD"),
                ],
            },
            "pipelines": {
                "ai": {
                    "ai_model": "gpt-oss:20B",
                    "valid_local_ai_models": [
                        "gpt-oss:20B",
                        "mistral-small3.1:24b",
                    ],
                }
            },
        }
        log.info(f"Content TOML payload prepared with {len(payload['program']['paths'])} configured paths.")
        return payload

    def generate_user(self) -> dict[str, Any]:
        return {
            "name": self.fake.name(),
            "email": self.fake.email(),
            "contacts": {
                self.fake.user_name(): {
                    "nickname": self.fake.first_name(),
                    "email": self.fake.email(),
                    "phone": self.fake.phone_number(),
                }
            },
        }

    def build_users_payload(self, count: int = 10) -> list[dict[str, Any]]:
        log.info(f"Generating JSON payload with {count} fake users.")
        users = [self.generate_user() for _ in range(count)]
        log.info(f"JSON payload prepared with {len(users)} generated users.")
        return users

    def run(self) -> None:
        self.configure_logger()
        log.info("Starting static IO test run.")
        log.info(
            f"Using test files SETTINGS={self.tmp_settings_toml}, CONTENT={self.tmp_content_toml}, JSON={self.tmp_json}."
        )

        settings_payload = self.build_settings_payload()
        content_payload = self.build_content_payload()
        users_payload = self.build_users_payload()

        log.info(f"Writing settings TOML test data to {self.tmp_settings_toml}.")
        write_toml(
            self.tmp_settings_toml,
            settings_payload,
            create_if_missing=True,
            on_error="raise",
        )
        log.info(f"Settings TOML test data written successfully to {self.tmp_settings_toml}.")

        log.info(f"Writing content TOML test data to {self.tmp_content_toml}.")
        write_toml(
            self.tmp_content_toml,
            content_payload,
            create_if_missing=True,
            on_error="raise",
        )
        log.info(f"Content TOML test data written successfully to {self.tmp_content_toml}.")

        log.info("Loading merged configuration from both TOML files.")
        config = load_config_files(self.tmp_settings_toml, self.tmp_content_toml)
        log.info(
            "Merged config loaded: pipelines.ai.enabled=%s, pipelines.ai.ai_model=%s",
            config.pipelines.ai.enabled,
            config.pipelines.ai.ai_model,
        )

        log.info(f"Writing JSON test data to {self.tmp_json}.")
        write_json(self.tmp_json, users_payload, create_if_missing=True, on_error="raise")
        log.info(f"JSON test data written successfully to {self.tmp_json}.")

        log.info(f"Reading JSON test data from {self.tmp_json}.")
        read_json(self.tmp_json, on_error="raise")
        log.info(f"JSON test data read successfully from {self.tmp_json}.")

        log.info("Static IO test run finished successfully.")


if __name__ == "__main__":
    StaticTestRunner().run()