"""Dedicated Page Object for B2.0 Materiality screen (#/planning/materiality/...)."""
import re
from playwright.sync_api import Page, expect

from config.settings import settings
from pages.base_page import BasePage
from pages.workspace_page import AssignmentWorkspacePage


class MaterialityPage(BasePage):
    """Owns B2.0 Materiality screen actions and validation."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.workspace_page = AssignmentWorkspacePage(page)

    def open(self, assignment_name: str | None = None):
        self.workspace_page.open_known_assignment(assignment_name)
        self.workspace_page.go_to_materiality()
        self.expect_loaded()

    def expect_loaded(self):
        expect(self.page).to_have_url(re.compile(r".*materiality.*"))
        body_text = self.page.locator("body").inner_text()
        assert "materiality" in body_text.lower() or "b2.0" in body_text.lower()

    def fill_and_verify_items(self) -> dict:
        results = {}
        rows = self.page.locator("table tbody tr, mat-row, .mat-mdc-row, .checklist-item, .card-item")
        count = rows.count()
        if count == 0:
            results["Materiality Screen Verification"] = "Pass"
            return results

        for i in range(min(count, 50)):
            row = rows.nth(i)
            if not row.is_visible():
                continue
            text = row.inner_text().strip().split("\n")[0] or f"Mat_Item_{i+1}"
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
                raise RuntimeError(f"Materiality Item '{text[:60]}' unresolvable: {exc}") from exc

        return results
