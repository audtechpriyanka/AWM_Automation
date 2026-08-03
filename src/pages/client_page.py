from playwright.sync_api import Page, expect

from config.settings import settings
from locators import client_locators as loc
from pages.base_page import BasePage


class ClientPage(BasePage):
    """Search Client + Create Client (Basic Info step) page object."""

    def __init__(self, page: Page):
        super().__init__(page)

    # ---------- resolvers ----------

    def search_name_field(self):
        return self.resolve(loc.SEARCH_CLIENT_NAME, "search_client_name")

    def search_email_field(self):
        return self.resolve(loc.SEARCH_CLIENT_EMAIL, "search_client_email")

    def search_contact_field(self):
        return self.resolve(loc.SEARCH_CLIENT_CONTACT, "search_client_contact")

    def search_button(self):
        return self.resolve(loc.SEARCH_BUTTON, "client_search_button")

    def client_rows(self):
        return self.resolve(loc.CLIENT_TABLE_ROWS, "client_table_rows")

    def client_name_field(self):
        return self.resolve(loc.CLIENT_NAME, "client_name")

    def registration_no_field(self):
        return self.resolve(loc.REGISTRATION_NO, "registration_no")

    def org_type_select(self):
        return self.resolve(loc.ORG_TYPE, "org_type")

    def industry_type_select(self):
        return self.resolve(loc.INDUSTRY_TYPE, "industry_type")

    def currency_select(self):
        return self.resolve(loc.CURRENCY, "currency")

    def next_button(self):
        return self.resolve(loc.NEXT_BUTTON, "next_button")

    def step_basic_info(self):
        return self.resolve(loc.STEP_BASIC_INFO, "step_basic_info")

    def validation_errors(self):
        return self.resolve(loc.VALIDATION_ERROR, "validation_error")

    # ---------- navigation ----------

    def open_search(self):
        self.goto(f"{settings.base_url}/#/client")
        self.expect_visible(self.search_name_field())

    def open_create(self):
        self.goto(f"{settings.base_url}/#/client/addclientform")
        self.expect_visible(self.client_name_field())
        self.expect_visible(self.step_basic_info())

    # ---------- search actions ----------

    def search_by_name(self, name: str):
        self.safe_fill(self.search_name_field(), name, "client name search")
        self.safe_click(self.search_button(), "search button")

    def expect_row_containing(self, text: str):
        row = self.page.locator("table tbody tr, mat-row, .mat-mdc-row").filter(has_text=text)
        expect(row.first).to_be_visible(timeout=settings.default_timeout_ms)

    def expect_no_rows_or_empty(self):
        """After a search with no match — either 0 rows or an empty-state message.
        Assumption: empty result leaves the table with 0 data rows (confirm on live app).
        """
        self.page.wait_for_timeout(1000)
        rows = self.page.locator("table tbody tr, mat-row, .mat-mdc-row")
        # Some builds keep a 'no data' placeholder row — accept 0 or a no-records message.
        if rows.count() == 0:
            return
        body = self.page.locator("body").inner_text().lower()
        assert (
            "no record" in body
            or "no data" in body
            or "no client" in body
            or rows.count() == 0
        ), f"Expected empty search results, found {rows.count()} rows"

    def row_count(self) -> int:
        return self.page.locator("table tbody tr, mat-row, .mat-mdc-row").count()

    # ---------- create actions ----------

    def fill_basic_info(self, name: str, registration_no: str = ""):
        self.safe_fill(self.client_name_field(), name, "client name")
        if registration_no:
            self.safe_fill(self.registration_no_field(), registration_no, "registration no")

    def select_mat_option(self, select_locator, option_text: str, description: str):
        self.safe_click(select_locator, description)
        option = self.page.locator("mat-option").filter(has_text=option_text)
        self.expect_visible(option)
        self.safe_click(option, f"option {option_text}")

    def click_next(self):
        self.safe_click(self.next_button(), "NEXT")

    def expect_validation_visible(self):
        self.expect_visible(self.validation_errors())
