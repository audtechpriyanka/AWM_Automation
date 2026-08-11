"""Profile and Change Password navigation, reached through the header user menu."""
from playwright.sync_api import Page

from config.settings import settings
from locators import profile_locators as loc
from pages.base_page import BasePage


class ProfilePage(BasePage):
    """Owns profile actions while preserving DashboardPage compatibility delegates."""

    def __init__(self, page: Page):
        super().__init__(page)

    def user_menu_button(self):
        return self.resolve(loc.USER_MENU_BUTTON, "user_menu_button")

    def profile_menu_item(self):
        return self.resolve(loc.PROFILE_MENU_ITEM, "profile_menu_item")

    def change_password_menu_item(self):
        return self.resolve(loc.CHANGE_PASSWORD_MENU_ITEM, "change_password_menu_item")

    def profile_image_input(self):
        return self.resolve(loc.PROFILE_IMAGE_INPUT, "profile_image_input")

    def profile_image_crop_button(self):
        return self.resolve(loc.PROFILE_IMAGE_CROP_BUTTON, "profile_image_crop_button")

    def profile_image_preview(self):
        return self.resolve(loc.PROFILE_IMAGE_PREVIEW, "profile_image_preview")

    def remove_photo_button(self):
        return self.resolve(loc.REMOVE_PHOTO_BUTTON, "remove_photo_button")

    def profile_update_button(self):
        return self.resolve(loc.PROFILE_UPDATE_BUTTON, "profile_update_button")

    def open_user_menu(self):
        self.safe_click(self.user_menu_button(), "user menu button")
        self.expect_visible(self.profile_menu_item())

    def open_profile(self):
        self.open_user_menu()
        self.safe_click(self.profile_menu_item(), "Profile")

    def open_change_password(self):
        self.open_user_menu()
        self.safe_click(self.change_password_menu_item(), "Change Password")

    def upload_profile_image(self, file_path: str):
        self.safe_upload(self.profile_image_input(), file_path, "profile image")
        self.expect_visible(self.profile_image_crop_button())
        self.safe_click(self.profile_image_crop_button(), "crop profile image")
        self.expect_visible(self.profile_image_preview())
        self.expect_visible(self.remove_photo_button())

    def save_profile(self):
        self.safe_click(self.profile_update_button(), "profile update")
        self.screenshot("profile_saved")

    def remove_profile_image(self):
        self.safe_click(self.remove_photo_button(), "remove profile image")
        self.expect_visible(self.profile_image_input())

    def reload_profile(self):
        self.goto(f"{settings.base_url}/#/user-profile")
        self.expect_visible(self.profile_update_button())

    def expect_profile_image_present(self):
        self.expect_visible(self.profile_image_preview())
        self.expect_visible(self.remove_photo_button())

    def expect_profile_image_removed(self):
        preview_count = loc.PROFILE_IMAGE_PREVIEW[0](self.page).count()
        assert preview_count == 0, "Profile image is still rendered after removal"
        self.expect_visible(self.profile_image_input())
