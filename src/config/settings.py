"""
Centralized configuration. Everything reads from environment variables
(.env locally, real env vars in CI) — never hardcode values in page
objects or tests. Import `settings` and use its attributes.
"""
import os
from dataclasses import dataclass
from typing import Dict, Tuple
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
    manager_username: str = os.getenv("MANAGER_USERNAME", "")
    manager_password: str = os.getenv("MANAGER_PASSWORD", "")
    partner_username: str = os.getenv("PARTNER_USERNAME", "")
    partner_password: str = os.getenv("PARTNER_PASSWORD", "")
    org_admin_username: str = os.getenv("ORG_ADMIN_USERNAME", "")
    org_admin_password: str = os.getenv("ORG_ADMIN_PASSWORD", "")

    profile_image_path: str = os.getenv("PROFILE_IMAGE_PATH") or os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "assets", "default_profile_image.png"
    )

    # Known UAT fixtures used by assignment-workspace / workflow tests.
    # Prefer names over hard-coded IDs — IDs rotate per assignment.
    known_client_name: str = os.getenv("KNOWN_CLIENT_NAME", "Apex Finserve Private Limited")
    known_assignment_name: str = os.getenv(
        "KNOWN_ASSIGNMENT_NAME", "Test AWMS_295 3.08.2026"
    )

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

    @property
    def role_credentials(self) -> Dict[str, Tuple[str, str]]:
        """Credentials for isolated workflow sessions; Org Admin is setup-only."""
        return {
            "priyanka": (self.valid_username, self.valid_password),
            "manager": (self.manager_username, self.manager_password),
            "partner": (self.partner_username, self.partner_password),
            "org_admin": (self.org_admin_username, self.org_admin_password),
        }


settings = Settings()
