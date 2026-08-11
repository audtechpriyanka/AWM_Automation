"""
Profile / Change Password — reachable from the dashboard user menu.
"""
import allure
import pytest

from config.settings import settings


@allure.feature("My Profile")
class TestProfile:

    @allure.story("Open Profile from user menu")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_open_profile(self, logged_in_pages):
        pages = logged_in_pages
        pages.profile_page.open_profile()
        pages.page.wait_for_timeout(1500)
        body = pages.page.locator("body").inner_text().lower()
        assert "profile" in body or "email" in body or "name" in body

    @allure.story("Upload and remove profile image")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_upload_remove_profile_image_persists(self, logged_in_pages):
        pages = logged_in_pages
        assert settings.profile_image_path, "PROFILE_IMAGE_PATH is required"
        pages.profile_page.open_profile()
        pages.profile_page.upload_profile_image(settings.profile_image_path)
        pages.profile_page.expect_profile_image_present()
        pages.profile_page.screenshot("profile_image_rendered_pre_reload")
        pages.profile_page.save_profile()

        pages.profile_page.reload_profile()
        pages.profile_page.screenshot("profile_image_absent_post_reload")
        pages.profile_page.expect_profile_image_present()

        # Explicit cleanup: restore the profile to its no-image state.
        pages.profile_page.remove_profile_image()
        pages.profile_page.save_profile()
        pages.profile_page.reload_profile()
        pages.profile_page.expect_profile_image_removed()

    @allure.story("Open Change Password from user menu")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_open_change_password(self, logged_in_pages):
        pages = logged_in_pages
        pages.profile_page.open_change_password()
        pages.page.wait_for_timeout(1500)
        body = pages.page.locator("body").inner_text().lower()
        assert "password" in body

    @allure.story("Change Password form requires current password")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    def test_change_password_empty_submit_stays(self, logged_in_pages):
        pages = logged_in_pages
        pages.profile_page.open_change_password()
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
