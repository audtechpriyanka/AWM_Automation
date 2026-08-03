from playwright.sync_api import Page

from config.settings import settings
from locators import login_locators as loc
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Reference implementation for how every future page object should be
    built:
      - inherit BasePage
      - locators come from src/locators/<page>_locators.py as fallback
        lists, resolved via self.resolve(...)
      - actions use safe_click / safe_fill (self-healing + logged)
      - no hardcoded values — everything from config.settings
    """

    def __init__(self, page: Page):
        super().__init__(page)

    def navigate(self):
        self.goto(settings.login_url)

    def username_field(self):
        return self.resolve(loc.USERNAME_FIELD, "username_field")

    def password_field(self):
        return self.resolve(loc.PASSWORD_FIELD, "password_field")

    def sign_in_button(self):
        return self.resolve(loc.SIGN_IN_BUTTON, "sign_in_button")

    def error_message(self):
        return self.resolve(loc.ERROR_MESSAGE, "error_message")

    def logo(self):
        return self.resolve(loc.LOGO, "logo")

    def login(self, username: str, password: str):
        self.safe_fill(self.username_field(), username, "username field")
        self.safe_fill(self.password_field(), password, "password field")
        self.screenshot("before_sign_in_click")
        self.safe_click(self.sign_in_button(), "sign in button")
        self.screenshot("after_sign_in_click")

    def expect_login_error(self, text: str = "Invalid Credentials"):
        self.expect_text(self.error_message(), text)
