"""
Dashboard / session tests — logout + sidenav navigation.
"""
import allure
import pytest

from config.settings import settings


@allure.feature("Dashboard")
class TestDashboard:

    @allure.story("Dashboard loads after login")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_dashboard_loaded(self, logged_in_pages):
        pages = logged_in_pages
        pages.dashboard_page.expect_dashboard_content()
        pages.dashboard_page.expect_visible(pages.dashboard_page.user_menu_button())

    @allure.story("Logout returns to login")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_logout(self, logged_in_pages):
        pages = logged_in_pages
        pages.dashboard_page.logout()
        pages.login_page.expect_visible(pages.login_page.logo())
        pages.login_page.expect_visible(pages.login_page.sign_in_button())

    @allure.story("User menu exposes profile actions")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_user_menu_items_visible(self, logged_in_pages):
        pages = logged_in_pages
        pages.dashboard_page.open_user_menu()
        pages.dashboard_page.expect_visible(pages.dashboard_page.profile_menu_item())
        pages.dashboard_page.expect_visible(pages.dashboard_page.change_password_menu_item())
        pages.dashboard_page.expect_visible(pages.dashboard_page.logout_menu_item())

    @allure.story("Sidenav — Client routes")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_navigate_create_and_search_client(self, logged_in_pages):
        pages = logged_in_pages
        pages.dashboard_page.go_to_create_client()
        pages.dashboard_page.go_to_search_client()

    @allure.story("Sidenav — Assignment routes")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_navigate_assignment_routes(self, logged_in_pages):
        pages = logged_in_pages
        pages.dashboard_page.go_to_create_assignment()
        pages.dashboard_page.go_to_search_assignment()
        pages.dashboard_page.go_to_archived_assignment()

    @allure.story("Sidenav — return to dashboard")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_navigate_back_to_dashboard(self, logged_in_pages):
        pages = logged_in_pages
        pages.dashboard_page.go_to_search_client()
        pages.dashboard_page.go_to_dashboard()
        pages.dashboard_page.expect_dashboard_content()

    @allure.story("Logout then re-login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_logout_then_login_again(self, logged_in_pages):
        pages = logged_in_pages
        pages.dashboard_page.logout()
        pages.login_page.login(settings.valid_username, settings.valid_password)
        pages.dashboard_page.is_loaded()
