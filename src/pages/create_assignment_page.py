"""Dedicated Page Object for Create Assignment screen (#/assignment/create)."""
from playwright.sync_api import Page, expect

from config.settings import settings
from locators import assignment_locators as loc
from pages.base_page import BasePage


class CreateAssignmentPage(BasePage):
    """Owns engagement creation screen actions and validation."""

    def __init__(self, page: Page):
        super().__init__(page)

    def assignment_name_field(self):
        return self.resolve(loc.ASSIGNMENT_NAME, "assignment_name")

    def client_field(self):
        return self.resolve(loc.CLIENT, "assignment_client")

    def assignment_type_select(self):
        return self.resolve(loc.ASSIGNMENT_TYPE, "assignment_type")

    def assignee_select(self):
        return self.resolve(loc.ASSIGNEE, "assignment_assignee")

    def start_date_field(self):
        return self.resolve(loc.START_DATE, "start_date")

    def end_date_field(self):
        return self.resolve(loc.END_DATE, "end_date")

    def create_button(self):
        return self.resolve(loc.CREATE_BUTTON, "create_button")

    def open(self):
        self.goto(f"{settings.base_url}/#/assignment/create")
        self.expect_form_loaded()

    def expect_form_loaded(self):
        self.expect_visible(self.assignment_name_field())
        self.expect_visible(self.client_field())
        self.expect_visible(self.assignment_type_select())
        self.expect_visible(self.create_button())

    def fill_assignment_name(self, name: str):
        self.safe_fill(self.assignment_name_field(), name, "assignment name")

    def select_client(self, client_name: str):
        self.safe_click(self.client_field(), "client field")
        self.safe_fill(self.client_field(), client_name, "client autocomplete")
        option = self.page.locator("mat-option, .mat-mdc-option").filter(has_text=client_name)
        self.expect_visible(option.first)
        self.safe_click(option.first, f"client {client_name}")

    def select_assignment_type(self, type_label: str):
        self.safe_click(self.assignment_type_select(), "assignment type")
        option = self.page.locator("mat-option").filter(has_text=type_label)
        self.expect_visible(option.first)
        self.safe_click(option.first, f"type {type_label}")

    def set_fy_dates(self, start_date: str = "01-04-2025", end_date: str = "31-03-2026"):
        """Fill FY start and end dates handling readonly datepicker inputs."""
        js_set_val = """(el, val) => {
            el.removeAttribute('readonly');
            el.value = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }"""
        if self.start_date_field().count() > 0:
            self.start_date_field().first.evaluate(js_set_val, start_date)
        if self.end_date_field().count() > 0:
            self.end_date_field().first.evaluate(js_set_val, end_date)

    def click_create(self):
        self.safe_click(self.create_button(), "CREATE")

    def expect_create_disabled(self):
        expect(self.create_button().first).to_be_disabled(timeout=settings.default_timeout_ms)
