"""
Centralized configuration. Everything reads from environment variables
(.env locally, real env vars in CI) — never hardcode values in page
objects or tests. Import `settings` and use its attributes.
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _bool(name: str, default: bool) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


def _int(name: str, default: int) -> int:
    val = os.getenv(name)
    try:
        return int(val) if val else default
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://audit-uat.audtech.co.in")
    login_path: str = os.getenv("LOGIN_PATH", "/#/login")
    dashboard_path: str = os.getenv("DASHBOARD_PATH", "/#/dashboard")

    valid_username: str = os.getenv("VALID_USERNAME", "")
    valid_password: str = os.getenv("VALID_PASSWORD", "")
    invalid_username: str = os.getenv("INVALID_USERNAME", "")
    invalid_password: str = os.getenv("INVALID_PASSWORD", "")
    old_password: str = os.getenv("OLD_PASSWORD", "")

    headless: bool = _bool("HEADLESS", True)
    slow_mo_ms: int = _int("SLOW_MO_MS", 0)
    default_timeout_ms: int = _int("DEFAULT_TIMEOUT_MS", 15000)
    nav_timeout_ms: int = _int("NAV_TIMEOUT_MS", 30000)
    viewport_width: int = _int("VIEWPORT_WIDTH", 1440)
    viewport_height: int = _int("VIEWPORT_HEIGHT", 900)

    max_action_retries: int = _int("MAX_ACTION_RETRIES", 2)
    retry_backoff_ms: int = _int("RETRY_BACKOFF_MS", 1000)

    @property
    def login_url(self) -> str:
        return f"{self.base_url}{self.login_path}"

    @property
    def dashboard_url(self) -> str:
        return f"{self.base_url}{self.dashboard_path}"


settings = Settings()
