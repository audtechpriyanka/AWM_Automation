"""Test suite for CreateAssignmentPage (#/assignment/create)."""
import allure
import pytest
from datetime import datetime

from pages.create_assignment_page import CreateAssignmentPage


@allure.feature("Create Assignment Screen")
class TestCreateAssignment:

    @allure.story("Create assignment form loads cleanly")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_create_assignment_form_loads(self, logged_in_pages):
        create_pg = CreateAssignmentPage(logged_in_pages.page)
        create_pg.open()
        create_pg.expect_form_loaded()

    @allure.story("Create button is disabled when required fields are empty")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.negative
    def test_create_disabled_when_empty(self, logged_in_pages):
        create_pg = CreateAssignmentPage(logged_in_pages.page)
        create_pg.open()
        create_pg.expect_create_disabled()

    @allure.story("Fill assignment name and FY dates")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_fill_assignment_name_and_fy_dates(self, logged_in_pages):
        create_pg = CreateAssignmentPage(logged_in_pages.page)
        create_pg.open()
        stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        create_pg.fill_assignment_name(f"AutoQA Create {stamp}")
        create_pg.set_fy_dates("01-04-2025", "31-03-2026")
        create_pg.select_assignment_type("Audit Workflow Management")
        create_pg.expect_form_loaded()
