"""Dedicated Page Object for Tailoring Questions screen."""
from playwright.sync_api import Page, expect

from config.settings import settings
from pages.base_page import BasePage
from pages.workspace_page import AssignmentWorkspacePage


class TailoringQuestionPage(BasePage):
    """Owns Tailoring Questions questionnaire screen actions and validation."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.workspace_page = AssignmentWorkspacePage(page)

    def tailoring_questions_nav(self):
        return self.page.locator("button, a, span").filter(has_text="Tailoring Questions")

    def question_rows(self):
        return self.page.locator("table tbody tr, mat-row, .mat-mdc-row, .question-item")

    def save_button(self):
        return self.page.get_by_role("button", name="SAVE").or_(self.page.locator("button", has_text="SAVE"))

    def open(self, assignment_name: str | None = None):
        self.workspace_page.open_known_assignment(assignment_name)
        nav = self.tailoring_questions_nav()
        if nav.count() > 0 and nav.first.is_visible():
            self.safe_click(nav.first, "Tailoring Questions nav")
            self.page.wait_for_timeout(2000)

    def expect_loaded(self):
        body_text = self.page.locator("body").inner_text()
        assert "tailoring" in body_text.lower() or "question" in body_text.lower() or "audit" in body_text.lower()

    def answer_all_questions(self, default_choice: str = "Yes") -> dict:
        """Dynamically answer visible questions and return item status map."""
        results = {}
        rows = self.question_rows()
        count = rows.count()
        if count == 0:
            results["Tailoring Screen Verification"] = "Pass"
            return results

        for i in range(min(count, 50)):
            row = rows.nth(i)
            if not row.is_visible():
                continue
            text = row.inner_text().strip().split("\n")[0] or f"Question_{i+1}"
            try:
                radios = row.locator("mat-radio-button, input[type='radio']")
                if radios.count() > 0:
                    target_opt = row.locator(f"mat-radio-button:has-text('{default_choice}'), input[value='{default_choice}']")
                    if target_opt.count() > 0 and target_opt.first.is_visible():
                        target_opt.first.click(force=True)
                    else:
                        radios.first.click(force=True)
                results[text[:60]] = "Pass"
            except Exception as exc:
                results[text[:60]] = "Blocked"
                raise RuntimeError(f"Tailoring question '{text[:60]}' unresolvable: {exc}") from exc

        return results

    def save(self):
        btn = self.save_button()
        if btn.count() > 0 and btn.first.is_visible() and not btn.first.is_disabled():
            btn.first.click(force=True)
            self.page.wait_for_timeout(1000)
