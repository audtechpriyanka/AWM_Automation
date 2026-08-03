from playwright.sync_api import Page, expect

from config.settings import settings
from locators import assignment_locators as loc
from pages.base_page import BasePage


class AssignmentPage(BasePage):
    """Search Assignment + Create Assignment page object."""

    def __init__(self, page: Page):
        super().__init__(page)

    # ---------- resolvers ----------

    def search_client_field(self):
        return self.resolve(loc.SEARCH_CLIENT, "assignment_search_client")

    def search_status_select(self):
        return self.resolve(loc.SEARCH_STATUS, "assignment_search_status")

    def search_type_select(self):
        return self.resolve(loc.SEARCH_TYPE, "assignment_search_type")

    def search_button(self):
        return self.resolve(loc.SEARCH_BUTTON, "assignment_search_button")

    def assignment_rows(self):
        return self.resolve(loc.ASSIGNMENT_TABLE_ROWS, "assignment_table_rows")

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

    def validation_errors(self):
        return self.resolve(loc.VALIDATION_ERROR, "assignment_validation_error")

    # ---------- navigation ----------

    def open_search(self):
        self.goto(f"{settings.base_url}/#/assignment")
        self.expect_visible(self.search_button())

    def open_create(self):
        self.goto(f"{settings.base_url}/#/assignment/create")
        self.expect_visible(self.assignment_name_field())
        self.expect_visible(self.create_button())

    # ---------- search ----------

    def search_by_client(self, client_name: str):
        self.safe_click(self.search_client_field(), "select client filter")
        self.safe_fill(self.search_client_field(), client_name, "client filter")
        option = self.page.locator("mat-option, .mat-mdc-option").filter(has_text=client_name)
        if option.count():
            self.safe_click(option.first, f"client option {client_name}")
        self.safe_click(self.search_button(), "search assignments")

    def filter_by_status(self, status_label: str):
        self.safe_click(self.search_status_select(), "status filter")
        option = self.page.locator("mat-option").filter(has_text=status_label)
        self.expect_visible(option)
        self.safe_click(option.first, f"status {status_label}")
        self.safe_click(self.search_button(), "search assignments")

    def expect_row_containing(self, text: str):
        row = self.page.locator("table tbody tr, mat-row, .mat-mdc-row").filter(has_text=text)
        expect(row.first).to_be_visible(timeout=settings.default_timeout_ms)

    def row_count(self) -> int:
        return self.page.locator("table tbody tr, mat-row, .mat-mdc-row").count()

    def open_assignment_by_name(self, name: str):
        link = self.page.get_by_role("link", name=name)
        if link.count() == 0:
            link = self.page.locator("a, button, td, mat-cell").filter(has_text=name)
        self.safe_click(link.first, f"open assignment {name}")

    # ---------- create ----------

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

    def select_assignee(self, assignee_label: str):
        self.safe_click(self.assignee_select(), "assignee")
        option = self.page.locator("mat-option").filter(has_text=assignee_label)
        self.expect_visible(option.first)
        # Multi-select: click option then close overlay
        self.safe_click(option.first, f"assignee {assignee_label}")
        self.page.keyboard.press("Escape")

    def click_create(self):
        self.safe_click(self.create_button(), "CREATE")

    def expect_validation_visible(self):
        # Assumption: submitting empty form surfaces mat-error or keeps user on create URL.
        errors = self.page.locator("mat-error, .mat-mdc-form-field-error")
        if errors.count() and errors.first.is_visible():
            return
        expect(self.page).to_have_url(f"{settings.base_url}/#/assignment/create")
