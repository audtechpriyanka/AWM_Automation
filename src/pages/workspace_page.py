from playwright.sync_api import Page, expect

from config.settings import settings
from locators import workspace_locators as loc
from pages.base_page import BasePage


class AssignmentWorkspacePage(BasePage):
    """
    Inside an opened AWM assignment: section sidenav + header tool menus.
    Open via open_known_assignment() (search list) rather than hard-coded IDs.
    """

    def __init__(self, page: Page):
        super().__init__(page)

    # ---------- resolvers ----------

    def section_risk_planning(self):
        return self.resolve(loc.SECTION_RISK_PLANNING, "section_risk_planning")

    def section_fieldwork(self):
        return self.resolve(loc.SECTION_FIELDWORK, "section_fieldwork")

    def section_reporting(self):
        return self.resolve(loc.SECTION_REPORTING, "section_reporting")

    def nav_materiality(self):
        return self.resolve(loc.NAV_MATERIALITY, "nav_materiality")

    def nav_planning_checklist(self):
        return self.resolve(loc.NAV_PLANNING_CHECKLIST, "nav_planning_checklist")

    def nav_budget(self):
        return self.resolve(loc.NAV_BUDGET, "nav_budget")

    def nav_risk_database(self):
        return self.resolve(loc.NAV_RISK_DATABASE, "nav_risk_database")

    def header_trial_balance(self):
        return self.resolve(loc.HEADER_TRIAL_BALANCE, "header_trial_balance")

    def header_templates(self):
        return self.resolve(loc.HEADER_TEMPLATES, "header_templates")

    def header_client_queries(self):
        return self.resolve(loc.HEADER_CLIENT_QUERIES, "header_client_queries")

    def header_audit_journal(self):
        return self.resolve(loc.HEADER_AUDIT_JOURNAL, "header_audit_journal")

    def header_sampling(self):
        return self.resolve(loc.HEADER_SAMPLING, "header_sampling")

    def header_sign_off(self):
        return self.resolve(loc.HEADER_SIGN_OFF, "header_sign_off")

    # ---------- open workspace ----------

    def open_known_assignment(self, name: str | None = None):
        """Open assignment by clicking span.assignment-name.clickable.

        Raises AssertionError if the name is not on the search list.
        (Do not silently fall back — that breaks negative tests.)
        """
        target = name or settings.known_assignment_name
        self.goto(f"{settings.base_url}/#/assignment")
        self.page.wait_for_timeout(1500)
        name_span = self.page.locator("span.assignment-name.clickable").filter(has_text=target)
        if name_span.count() == 0:
            raise AssertionError(f"No assignment row found for '{target}'")
        self.safe_click(name_span.first, f"open assignment {target}")
        # Hash routes: assert workspace chrome rather than wait_for_url globs.
        self.expect_visible(self.header_trial_balance())
        self.expect_visible(self.header_sign_off())

    def _ensure_risk_planning_expanded(self):
        probe = self.page.locator("a.sidenav-item").filter(has_text="Materiality")
        if probe.count() == 0 or not probe.first.is_visible():
            section = self.page.locator("a.sidenav-item").filter(has_text="B-Risk Assessment")
            self.safe_click(section.first, "expand B-Risk Assessment & Planning")
            self.page.wait_for_timeout(800)
        self.expect_visible(self.page.locator("a.sidenav-item").filter(has_text="Materiality"))

    def _click_sidenav_item(self, text: str, description: str):
        self._ensure_risk_planning_expanded()
        item = self.page.locator("a.sidenav-item").filter(has_text=text)
        self.expect_visible(item)
        item.first.scroll_into_view_if_needed()
        self.safe_click(item.first, description)
        self.page.wait_for_timeout(1500)

    # ---------- navigations ----------

    def go_to_materiality(self):
        self._click_sidenav_item("Materiality", "Materiality")
        self.expect_page_contains("Materiality")

    def go_to_planning_checklist(self):
        self._click_sidenav_item("Planning Checklist", "Planning Checklist")
        self.expect_page_contains("Checklist")

    def go_to_budget(self):
        # Prefer the planning budget (B12); avoid matching D5 budget.
        self._click_sidenav_item("B12.0 - Budget", "Budget")
        self.expect_page_contains("Budget")

    def go_to_risk_database(self):
        self._click_sidenav_item("Audit Risk Database", "Audit Risk Database")
        self.expect_page_contains("Risk")

    def go_to_trial_balance(self):
        self.safe_click(self.header_trial_balance(), "Trial Balance")
        self.page.wait_for_timeout(2000)

    def go_to_templates(self):
        self.safe_click(self.header_templates(), "Templates")
        self.page.wait_for_timeout(2000)

    def go_to_client_queries(self):
        self.safe_click(self.header_client_queries(), "Client Queries")
        self.page.wait_for_timeout(2000)

    def go_to_audit_journal(self):
        self.safe_click(self.header_audit_journal(), "Audit Journal")
        self.page.wait_for_timeout(2000)

    def go_to_sampling(self):
        self.safe_click(self.header_sampling(), "Sampling")
        self.page.wait_for_timeout(2000)

    def open_sign_off_menu(self):
        self.safe_click(self.header_sign_off(), "Sign-Off")
        self.page.wait_for_timeout(500)

    def expect_sign_off_menu_open(self):
        panel = self.page.locator(".mat-mdc-menu-panel, [role='menu']").first
        self.expect_visible(panel)
        text = panel.inner_text().lower()
        assert "planning" in text or "field" in text or "completion" in text or "sign" in text

    def expect_page_contains(self, text: str):
        expect(self.page.locator("body")).to_contain_text(text, timeout=settings.default_timeout_ms)
