import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from playwright.sync_api import Page

from config.settings import settings
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.logger import get_logger
from utilities.screenshots import capture_screenshot

logger = get_logger("conftest")

try:
    import allure
    ALLURE_AVAILABLE = True
except ImportError:
    ALLURE_AVAILABLE = False


# ---------- Playwright browser/context configuration ----------

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": settings.headless,
        "slow_mo": settings.slow_mo_ms,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": settings.viewport_width, "height": settings.viewport_height},
        "accept_downloads": True,
    }


@pytest.fixture(autouse=True)
def _set_default_timeout(page: Page):
    page.set_default_timeout(settings.default_timeout_ms)
    yield


# ---------- Page Object Manager ----------

class PageManager:
    """
    Instantiates every page object once per test via the `pages` fixture.
    Add a new page object here as soon as it's created — this is the
    single place tests reach through to get to any page.
    """

    def __init__(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)
        # Add new page objects here as the agent builds them out, e.g.:
        # self.add_client_page = AddClientPage(page)
        # self.trial_balance_page = TrialBalancePage(page)


@pytest.fixture
def pages(page: Page) -> PageManager:
    return PageManager(page)


@pytest.fixture
def logged_in_pages(pages: PageManager) -> PageManager:
    """Convenience fixture: navigates to login and signs in with valid
    credentials from settings, returns the PageManager already authenticated."""
    pages.login_page.navigate()
    pages.login_page.login(settings.valid_username, settings.valid_password)
    pages.dashboard_page.is_loaded()
    return pages


@pytest.fixture
def download_dir(tmp_path):
    d = tmp_path / "downloads"
    d.mkdir()
    yield str(d)


# ---------- Screenshot-on-failure + Allure attachment ----------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = None
        # `page` fixture may or may not have been requested by the test
        if "page" in item.funcargs:
            page = item.funcargs["page"]
        elif "pages" in item.funcargs:
            page = item.funcargs["pages"].page
        elif "logged_in_pages" in item.funcargs:
            page = item.funcargs["logged_in_pages"].page

        if page is not None:
            path = capture_screenshot(page, f"FAILURE_{item.name}")
            logger.error("Test failed: %s | screenshot: %s | url: %s", item.name, path, page.url)
