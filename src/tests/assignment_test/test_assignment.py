"""
Assignment management tests — search + create validation.
"""
import allure
import pytest
from datetime import datetime


KNOWN_CLIENT = "Apex Finserve Private Limited"


@allure.feature("Assignment Management")
class TestAssignment:

    @allure.story("Search assignment list loads")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_search_assignment_list_loads(self, logged_in_pages):
        pages = logged_in_pages
        pages.assignment_page.open_search()
        assert pages.assignment_page.row_count() > 0

    @allure.story("Filter assignments by status")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_filter_assignment_by_status(self, logged_in_pages):
        pages = logged_in_pages
        pages.assignment_page.open_search()
        pages.assignment_page.filter_by_status("Pending Review")
        pages.page.wait_for_timeout(1500)
        pages.assignment_page.expect_row_containing("Pending Review")

    @allure.story("Search by client name")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_search_assignment_by_client(self, logged_in_pages):
        pages = logged_in_pages
        pages.assignment_page.open_search()
        pages.assignment_page.search_by_client(KNOWN_CLIENT)
        pages.page.wait_for_timeout(1500)
        pages.assignment_page.expect_row_containing(KNOWN_CLIENT)

    @allure.story("Create assignment form loads")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_create_assignment_form_loads(self, logged_in_pages):
        pages = logged_in_pages
        pages.assignment_page.open_create()
        pages.assignment_page.expect_visible(pages.assignment_page.assignment_name_field())
        pages.assignment_page.expect_visible(pages.assignment_page.client_field())
        pages.assignment_page.expect_visible(pages.assignment_page.assignment_type_select())
        pages.assignment_page.expect_visible(pages.assignment_page.create_button())

    @allure.story("Create blocked when required fields empty")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.negative
    def test_create_assignment_requires_fields(self, logged_in_pages):
        pages = logged_in_pages
        pages.assignment_page.open_create()
        # Assumption confirmed on live app: CREATE stays disabled until required
        # fields are filled (clicking it times out when empty).
        from playwright.sync_api import expect
        expect(pages.assignment_page.create_button().first).to_be_disabled()

    @allure.story("Fill assignment name and select AWM type")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_select_awm_type_on_create(self, logged_in_pages):
        pages = logged_in_pages
        pages.assignment_page.open_create()
        stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        pages.assignment_page.fill_assignment_name(f"AutoQA Assign {stamp}")
        pages.assignment_page.select_assignment_type("Audit Workflow Management")
        # Assumption: selecting AWM reveals conditional fields (Amount Type / Roll Forward etc.)
        # We only assert the type control still shows and CREATE remains visible.
        pages.assignment_page.expect_visible(pages.assignment_page.create_button())
        body = pages.page.locator("body").inner_text()
        assert "Audit Workflow Management" in body or "Amount" in body
