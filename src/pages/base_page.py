"""
BasePage: every page object should inherit from this instead of
duplicating __init__/wait/click boilerplate. Keep page objects focused
on locators + business actions; put generic Playwright plumbing here.
"""
from typing import Callable, List, Optional

from playwright.sync_api import Locator, Page, expect

from config.settings import settings
from utilities.logger import get_logger
from utilities.screenshots import capture_screenshot
from utilities.self_healing import resolve_locator, self_heal


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    # ---------- navigation ----------

    def goto(self, url: str):
        self.logger.info("Navigating to %s", url)
        self.page.goto(url, timeout=settings.nav_timeout_ms)

    def current_url(self) -> str:
        return self.page.url

    # ---------- resilient element resolution ----------

    def resolve(self, strategies: List[Callable[[Page], Locator]], description: str) -> Locator:
        """Given ordered locator strategies, return the first that resolves.
        Use this in page objects for elements known to be flaky/renamed
        across app releases, e.g.:

            self.resolve([
                lambda p: p.get_by_role("button", name="SIGN IN"),
                lambda p: p.locator('button[type="submit"]'),
            ], "sign_in_button")
        """
        return resolve_locator(self.page, strategies, description)

    # ---------- actions (self-healing: retried + screenshotted on failure) ----------

    @self_heal()
    def safe_click(self, locator: Locator, description: str = ""):
        self.logger.info("Clicking: %s", description or locator)
        locator.first.wait_for(state="visible", timeout=settings.default_timeout_ms)
        locator.first.click()

    @self_heal()
    def safe_fill(self, locator: Locator, value: str, description: str = ""):
        self.logger.info("Filling '%s' into: %s", value, description or locator)
        locator.first.wait_for(state="visible", timeout=settings.default_timeout_ms)
        locator.first.fill(value)

    @self_heal()
    def safe_select(self, locator: Locator, label: Optional[str] = None, value: Optional[str] = None, description: str = ""):
        self.logger.info("Selecting option in: %s", description or locator)
        if label is not None:
            locator.first.select_option(label=label)
        elif value is not None:
            locator.first.select_option(value=value)
        else:
            raise ValueError("safe_select requires either label or value")

    @self_heal()
    def safe_upload(self, locator: Locator, file_path: str, description: str = ""):
        self.logger.info("Uploading '%s' via: %s", file_path, description or locator)
        locator.first.set_input_files(file_path)

    # ---------- waits / assertions ----------

    def wait_visible(self, locator: Locator, timeout: Optional[int] = None):
        locator.first.wait_for(state="visible", timeout=timeout or settings.default_timeout_ms)

    def expect_visible(self, locator: Locator, timeout: Optional[int] = None):
        expect(locator.first).to_be_visible(timeout=timeout or settings.default_timeout_ms)

    def expect_text(self, locator: Locator, text: str, timeout: Optional[int] = None):
        expect(locator.first).to_contain_text(text, timeout=timeout or settings.default_timeout_ms)

    def expect_url(self, url: str, timeout: Optional[int] = None):
        expect(self.page).to_have_url(url, timeout=timeout or settings.default_timeout_ms)

    # ---------- diagnostics ----------

    def screenshot(self, label: str) -> str:
        return capture_screenshot(self.page, label)

    def get_text(self, locator: Locator) -> str:
        return locator.first.inner_text().strip()
