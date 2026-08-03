"""
Screenshot capture used for: before/after key actions, and automatically
on any failure (see self_healing.py and tests/conftest.py's
pytest_runtest_makereport hook). Screenshots land in screenshots/ and,
when Allure is active, get attached to the test report too.
"""
import os
import re
import time

from playwright.sync_api import Page

SCREENSHOT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "screenshots"
)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def _safe_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", name)[:120]


def capture_screenshot(page: Page, label: str) -> str:
    """Save a screenshot and return its path. Never raises — a failed
    screenshot should not mask the real test failure."""
    try:
        filename = f"{_safe_name(label)}_{int(time.time() * 1000)}.png"
        path = os.path.join(SCREENSHOT_DIR, filename)
        page.screenshot(path=path, full_page=True)
        try:
            import allure
            allure.attach.file(
                path, name=label, attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass
        return path
    except Exception:
        return ""
