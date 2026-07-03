import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "User API")
    app_version: str = os.getenv("APP_VERSION", "2.0.0")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()


settings = Settings()

