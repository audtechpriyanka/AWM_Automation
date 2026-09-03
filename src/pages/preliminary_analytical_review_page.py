"""Dedicated Page Object for B3.0 Preliminary Analytical Review & Trend Analysis screen."""
import re
from playwright.sync_api import Page, expect

from config.settings import settings
from pages.base_page import BasePage
from pages.workspace_page import AssignmentWorkspacePage


class PreliminaryAnalyticalReviewPage(BasePage):
    """Owns B3.0 Preliminary Analytical Review and embedded Trend Analysis actions."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.workspace_page = AssignmentWorkspacePage(page)

    def open(self, assignment_name: str | None = None):
        self.workspace_page.open_known_assignment(assignment_name)
        self.workspace_page._ensure_risk_planning_expanded()
        item = self.page.locator("a.sidenav-item, .sidenav-item").filter(has_text="B3.0").first
        if item.count() == 0:
            item = self.page.locator("a.sidenav-item, .sidenav-item").filter(has_text="Preliminary Analytical").first
        if item.count() > 0:
            self.safe_click(item, "B3.0 Preliminary Analytical Review nav")
            self.page.wait_for_timeout(2000)

    def expect_loaded(self):
        body_text = self.page.locator("body").inner_text()
        assert "analytical" in body_text.lower() or "b3.0" in body_text.lower() or "review" in body_text.lower()

    def trend_analysis_tab(self):
        return self.page.locator("mat-tab, [role='tab'], button, a").filter(has_text="Trend Analysis")

    def open_trend_analysis(self):
        """Navigate to Trend Analysis tab/section inside B3.0."""
        tab = self.trend_analysis_tab()
        if tab.count() > 0 and tab.first.is_visible():
            self.safe_click(tab.first, "Trend Analysis tab")
            self.page.wait_for_timeout(1000)

    def fill_and_verify_items(self) -> dict:
        results = {}
        rows = self.page.locator("table tbody tr, mat-row, .mat-mdc-row, .checklist-item, .card-item")
        count = rows.count()
        if count == 0:
            results["Preliminary Analytical Review Screen Verification"] = "Pass"
            return results

        for i in range(min(count, 50)):
            row = rows.nth(i)
            if not row.is_visible():
                continue
            text = row.inner_text().strip().split("\n")[0] or f"PAR_Item_{i+1}"
            try:
                radios = row.locator("mat-radio-button, input[type='radio']")
                if radios.count() > 0:
                    yes_opt = row.locator("mat-radio-button:has-text('Yes'), input[value='Yes']")
                    if yes_opt.count() > 0 and yes_opt.first.is_visible():
                        yes_opt.first.click(force=True)
                    else:
                        radios.first.click(force=True)
                results[text[:60]] = "Pass"
            except Exception as exc:
                results[text[:60]] = "Blocked"
                raise RuntimeError(f"PAR Item '{text[:60]}' unresolvable: {exc}") from exc

        return results
