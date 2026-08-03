"""
Login test suite — reference template. Every future feature test module
should follow this shape:
  - one class per feature
  - @pytest.fixture(autouse=True) for shared pre-condition
  - @pytest.mark.<smoke|regression|positive|negative> per test
  - @allure.feature / @allure.story / @allure.severity for reporting
  - assertions via BasePage.expect_* (Playwright's own `expect`)
"""
import allure
import pytest

from config.settings import settings


@allure.feature("Authentication")
class TestLogin:

    @pytest.fixture(autouse=True)
    def before_each(self, pages):
        pages.login_page.navigate()
        pages.login_page.expect_visible(pages.login_page.logo())

    @allure.story("Valid login")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_valid_login(self, pages):
        pages.login_page.login(settings.valid_username, settings.valid_password)
        pages.dashboard_page.is_loaded()

    @allure.story("Invalid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.negative
    def test_invalid_username(self, pages):
        pages.login_page.login(settings.invalid_username or "not_a_real_user@audtech.co.in", settings.valid_password)
        pages.login_page.expect_login_error()

    @allure.story("Invalid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.negative
    def test_invalid_password(self, pages):
        pages.login_page.login(settings.valid_username, settings.invalid_password or "WrongPassword123")
        pages.login_page.expect_login_error()

    @allure.story("Sign-in button state")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    def test_signin_disabled_when_empty(self, pages):
        pages.login_page.expect_visible(pages.login_page.sign_in_button())
        # Assumption: the button is disabled until both fields are non-empty.
        # Confirm on the live app; adjust to `.to_be_enabled()` check if the
        # button is always clickable but validates on click instead.
        from playwright.sync_api import expect
        expect(pages.login_page.sign_in_button().first).to_be_disabled()

    @allure.story("Old password rejected")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    def test_old_password_rejected(self, pages):
        if not settings.old_password:
            pytest.skip("OLD_PASSWORD not set in .env — nothing to test")
        pages.login_page.login(settings.valid_username, settings.old_password)
        pages.login_page.expect_login_error()
