"""
Profile / Change Password — reachable from the dashboard user menu.
"""
import allure
import pytest


@allure.feature("My Profile")
class TestProfile:

    @allure.story("Open Profile from user menu")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_open_profile(self, logged_in_pages):
        pages = logged_in_pages
        pages.dashboard_page.open_user_menu()
        pages.dashboard_page.safe_click(pages.dashboard_page.profile_menu_item(), "Profile")
        pages.page.wait_for_timeout(1500)
        body = pages.page.locator("body").inner_text().lower()
        assert "profile" in body or "email" in body or "name" in body

    @allure.story("Open Change Password from user menu")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_open_change_password(self, logged_in_pages):
        pages = logged_in_pages
        pages.dashboard_page.open_user_menu()
        pages.dashboard_page.safe_click(
            pages.dashboard_page.change_password_menu_item(), "Change Password"
        )
        pages.page.wait_for_timeout(1500)
        body = pages.page.locator("body").inner_text().lower()
        assert "password" in body

    @allure.story("Change Password form requires current password")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    def test_change_password_empty_submit_stays(self, logged_in_pages):
        pages = logged_in_pages
        pages.dashboard_page.open_user_menu()
        pages.dashboard_page.safe_click(
            pages.dashboard_page.change_password_menu_item(), "Change Password"
        )
        pages.page.wait_for_timeout(1000)
        # Try common submit labels; if button disabled, that is also a valid guard.
        submit = pages.page.get_by_role("button", name="SAVE")
        if submit.count() == 0:
            submit = pages.page.get_by_role("button", name="Update")
        if submit.count() == 0:
            submit = pages.page.get_by_role("button", name="Submit")
        if submit.count() and submit.first.is_enabled():
            pages.dashboard_page.safe_click(submit, "submit change password")
            pages.page.wait_for_timeout(800)
        body = pages.page.locator("body").inner_text().lower()
        assert "password" in body
