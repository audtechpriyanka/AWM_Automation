from playwright.sync_api import Page
import re

from config.settings import settings
from locators import dashboard_locators as loc
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """
    App shell: dashboard landing, header user menu, and left sidenav.
    Locators live in dashboard_locators.py — match LoginPage pattern.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.dashboard_page_url = settings.dashboard_url

    # ---------- element resolvers ----------

    def user_menu_button(self):
        return self.resolve(loc.USER_MENU_BUTTON, "user_menu_button")

    def logout_menu_item(self):
        return self.resolve(loc.LOGOUT_MENU_ITEM, "logout_menu_item")

    def profile_menu_item(self):
        return self.resolve(loc.PROFILE_MENU_ITEM, "profile_menu_item")

    def change_password_menu_item(self):
        return self.resolve(loc.CHANGE_PASSWORD_MENU_ITEM, "change_password_menu_item")

    def dashboard_heading(self):
        return self.resolve(loc.DASHBOARD_HEADING, "dashboard_heading")

    def sidenav_dashboard(self):
        return self.resolve(loc.SIDENAV_DASHBOARD, "sidenav_dashboard")

    def sidenav_client(self):
        return self.resolve(loc.SIDENAV_CLIENT, "sidenav_client")

    def sidenav_create_client(self):
        return self.resolve(loc.SIDENAV_CREATE_CLIENT, "sidenav_create_client")

    def sidenav_search_client(self):
        return self.resolve(loc.SIDENAV_SEARCH_CLIENT, "sidenav_search_client")

    def sidenav_assignment(self):
        return self.resolve(loc.SIDENAV_ASSIGNMENT, "sidenav_assignment")

    def sidenav_create_assignment(self):
        return self.resolve(loc.SIDENAV_CREATE_ASSIGNMENT, "sidenav_create_assignment")

    def sidenav_search_assignment(self):
        return self.resolve(loc.SIDENAV_SEARCH_ASSIGNMENT, "sidenav_search_assignment")

    def sidenav_archived_assignment(self):
        return self.resolve(loc.SIDENAV_ARCHIVED_ASSIGNMENT, "sidenav_archived_assignment")

    def recent_assignments_section(self):
        return self.resolve(loc.RECENT_ASSIGNMENTS_SECTION, "recent_assignments_section")

    def sidenav_toggle(self):
        return self.resolve(loc.SIDENAV_TOGGLE, "sidenav_toggle")

    # ---------- assertions / actions ----------

    def is_loaded(self) -> bool:
        self.expect_url(self.dashboard_page_url)
        return True

    def expect_dashboard_content(self):
        # Title is a div.crumb / currentPage, not always a heading role.
        self.expect_visible(self.recent_assignments_section())
        self.expect_visible(self.user_menu_button())

    def open_user_menu(self):
        self.safe_click(self.user_menu_button(), "user menu button")
        self.expect_visible(self.logout_menu_item())

    def logout(self):
        self.open_user_menu()
        self.screenshot("before_logout_click")
        self.safe_click(self.logout_menu_item(), "logout menu item")
        # Assumption: logout returns to the login route.
        self.expect_url(settings.login_url)

    def _ensure_client_expanded(self):
        # Sub-items only appear after expanding the Client group.
        # Do NOT resolve() the child first — resolve waits for visible and
        # fails while the group is collapsed.
        create = self.page.locator("a.sidenav-item[href='#/client/addclientform']")
        if create.count() == 0 or not create.first.is_visible():
            self.safe_click(self.sidenav_client(), "sidenav Client")
        self.expect_visible(self.sidenav_create_client())

    def _ensure_assignment_expanded(self):
        create = self.page.locator("a.sidenav-item[href='#/assignment/create']")
        if create.count() == 0 or not create.first.is_visible():
            self.safe_click(self.sidenav_assignment(), "sidenav Assignment")
        self.expect_visible(self.sidenav_create_assignment())

    def go_to_dashboard(self):
        self.safe_click(self.sidenav_dashboard(), "sidenav Dashboard")
        self.expect_url(self.dashboard_page_url)

    def go_to_create_client(self):
        self._ensure_client_expanded()
        self.safe_click(self.sidenav_create_client(), "Create Client")
        self.expect_url(f"{settings.base_url}/#/client/addclientform")

    def go_to_search_client(self):
        self._ensure_client_expanded()
        self.safe_click(self.sidenav_search_client(), "Search Client")
        self.page.wait_for_url(re.compile(r".*/#/client/?$"), timeout=settings.nav_timeout_ms)

    def go_to_create_assignment(self):
        self._ensure_assignment_expanded()
        self.safe_click(self.sidenav_create_assignment(), "Create Assignment")
        self.expect_url(f"{settings.base_url}/#/assignment/create")

    def go_to_search_assignment(self):
        self._ensure_assignment_expanded()
        self.safe_click(self.sidenav_search_assignment(), "Search Assignment")
        self.page.wait_for_url(re.compile(r".*/#/assignment/?$"), timeout=settings.nav_timeout_ms)

    def go_to_archived_assignment(self):
        self._ensure_assignment_expanded()
        self.safe_click(self.sidenav_archived_assignment(), "Archived Assignment")
        self.expect_url(f"{settings.base_url}/#/assignment/archived")
