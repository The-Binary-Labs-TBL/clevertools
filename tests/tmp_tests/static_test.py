from __future__ import annotations

from pathlib import Path
from typing import Any
from faker import Faker

from clevertools import configure, log, read_json, read_toml, write_json, write_toml
from ..paths import PATHS


class StaticTestRunner:
    def __init__(self) -> None:
        self.fake = Faker("de_DE")
        self.tmp_toml: Path = PATHS.CACHE_FOLDER / "config.toml"
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

    def build_toml_payload(self) -> dict[str, Any]:
        log.info("Building TOML payload for configuration test data.")
        payload = {
            "app": {
                "enviroment": "release",
                "wait_for_enter": True,
                "paths": [
                    PATHS.CACHE_FOLDER / "hello",
                    PATHS.CACHE_FOLDER / "world",
                    PATHS.CACHE_FOLDER / "my",
                    PATHS.CACHE_FOLDER / "name",
                    PATHS.CACHE_FOLDER / "is",
                    PATHS.CACHE_FOLDER / "b7binw13",
                    PATHS.CACHE_FOLDER / "yayxD",
                ],
            },
            "logger": {
                "name": "ClevertoolsStaticTest",
                "level": "INFO",
                "format_preset": "datetime",
                "file_logging_enabled": True,
                "file_log_path": PATHS.CACHE_FOLDER / "clevertools_static_test.log",
            },
        }
        log.info(f"TOML payload prepared with {len(payload['app']['paths'])} configured paths.")
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
            f"Using test files TOML={self.tmp_toml} and JSON={self.tmp_json}."
        )

        toml_payload = self.build_toml_payload()
        users_payload = self.build_users_payload()

        log.info(f"Writing TOML test data to {self.tmp_toml}.")
        write_toml(self.tmp_toml, toml_payload, create_if_missing=True)
        log.info(f"TOML test data written successfully to {self.tmp_toml}.")

        log.info(f"Reading TOML test data from {self.tmp_toml}.")
        read_toml(self.tmp_toml)
        log.info(f"TOML test data read successfully from {self.tmp_toml}.")

        log.info(f"Writing JSON test data to {self.tmp_json}.")
        write_json(self.tmp_json, users_payload, create_if_missing=True)
        log.info(f"JSON test data written successfully to {self.tmp_json}.")

        log.info(f"Reading JSON test data from {self.tmp_json}.")
        read_json(self.tmp_json)
        log.info(f"JSON test data read successfully from {self.tmp_json}.")

        log.info("Static IO test run finished successfully.")


if __name__ == "__main__":
    StaticTestRunner().run()