"""Dedicated Page Object for Trial Balance import screen (#/assignment/.../importtb)."""
from playwright.sync_api import Page, expect

from config.settings import settings
from pages.base_page import BasePage
from pages.workspace_page import AssignmentWorkspacePage


class TrialBalancePage(BasePage):
    """Owns Trial Balance import, preview, and save actions."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.workspace_page = AssignmentWorkspacePage(page)

    def file_input(self):
        return self.page.locator("input[type='file']")

    def choose_file_label(self):
        return self.page.locator("label").filter(has_text="CHOOSE FILE")

    def preview_button(self):
        return self.page.get_by_role("button", name="PREVIEW").or_(self.page.locator("button", has_text="PREVIEW"))

    def save_button(self):
        return self.page.get_by_role("button", name="SAVE").or_(self.page.locator("button", has_text="SAVE")).first

    def show_fsa_button(self):
        return self.page.get_by_role("button", name="SHOW FSA").or_(self.page.locator("button", has_text="SHOW FSA"))

    def download_tb_button(self):
        return self.page.get_by_role("button", name="DOWNLOAD TB").or_(self.page.locator("button", has_text="DOWNLOAD TB"))

    def open(self, assignment_name: str | None = None):
        self.workspace_page.open_known_assignment(assignment_name)
        self.workspace_page.go_to_trial_balance()
        self.expect_loaded()

    def expect_loaded(self):
        import re
        expect(self.page).to_have_url(re.compile(r".*importtb.*"))
        body_text = self.page.locator("body").inner_text()
        assert "trial" in body_text.lower() or "balance" in body_text.lower() or "choose file" in body_text.lower()

    def upload_tb_file(self, file_path: str):
        """Upload Trial Balance file via input[type='file']."""
        self.safe_upload(self.file_input(), file_path, "Trial Balance file input")
        self.page.wait_for_timeout(1000)

    def click_preview(self):
        btn = self.preview_button()
        if btn.count() > 0 and btn.first.is_visible():
            self.safe_click(btn.first, "PREVIEW Trial Balance")
            self.page.wait_for_timeout(1000)

    def click_save(self):
        btn = self.save_button()
        if btn.count() > 0 and btn.first.is_visible() and not btn.first.is_disabled():
            btn.first.click(force=True)
            self.page.wait_for_timeout(1000)
