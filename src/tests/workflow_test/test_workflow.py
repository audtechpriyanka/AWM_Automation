"""
Core audit workflow + related screens inside an opened AWM assignment.
"""
import allure
import pytest

from config.settings import settings


@pytest.fixture
def workspace(logged_in_pages):
    pages = logged_in_pages
    pages.workspace_page.open_known_assignment()
    return pages


@allure.feature("Audit Workflow")
class TestAuditWorkflow:

    @allure.story("Open known assignment workspace")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_open_assignment_workspace(self, workspace):
        pages = workspace
        pages.workspace_page.expect_visible(pages.workspace_page.header_trial_balance())
        pages.workspace_page.expect_visible(pages.workspace_page.header_sign_off())

    @allure.story("Navigate to Materiality")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_open_materiality(self, workspace):
        pages = workspace
        pages.workspace_page.go_to_materiality()
        pages.workspace_page.expect_page_contains("Materiality")

    @allure.story("Navigate to Planning Checklist")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_open_planning_checklist(self, workspace):
        pages = workspace
        pages.workspace_page.go_to_planning_checklist()
        pages.workspace_page.expect_page_contains("Checklist")

    @allure.story("Navigate to Audit Risk Database")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_open_risk_database(self, workspace):
        pages = workspace
        pages.workspace_page.go_to_risk_database()
        body = pages.page.locator("body").inner_text()
        assert "Risk" in body or "risk" in body.lower()

    @allure.story("Open Trial Balance from header")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_open_trial_balance(self, workspace):
        pages = workspace
        pages.workspace_page.go_to_trial_balance()
        body = pages.page.locator("body").inner_text().lower()
        assert "trial" in body or "balance" in body or "upload" in body or "account" in body

    @allure.story("Open Budget")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_open_budget(self, workspace):
        pages = workspace
        pages.workspace_page.go_to_budget()
        pages.workspace_page.expect_page_contains("Budget")

    @allure.story("Sign-Off menu opens")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_sign_off_menu(self, workspace):
        pages = workspace
        pages.workspace_page.open_sign_off_menu()
        pages.workspace_page.expect_sign_off_menu_open()

    @allure.story("Templates header tool")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_open_templates(self, workspace):
        pages = workspace
        pages.workspace_page.go_to_templates()
        body = pages.page.locator("body").inner_text().lower()
        assert "template" in body or "document" in body or "upload" in body

    @allure.story("Client Queries header tool")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_open_client_queries(self, workspace):
        pages = workspace
        pages.workspace_page.go_to_client_queries()
        body = pages.page.locator("body").inner_text().lower()
        assert "quer" in body or "client" in body

    @allure.story("Audit Journal header tool")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_open_audit_journal(self, workspace):
        pages = workspace
        pages.workspace_page.go_to_audit_journal()
        body = pages.page.locator("body").inner_text().lower()
        assert "journal" in body or "audit" in body

    @allure.story("Sampling header tool")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_open_sampling(self, workspace):
        pages = workspace
        pages.workspace_page.go_to_sampling()
        body = pages.page.locator("body").inner_text().lower()
        assert "sampl" in body or "population" in body or "size" in body or "method" in body

    @allure.story("Missing known assignment name fails clearly")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.negative
    def test_unknown_assignment_name_fails_clearly(self, logged_in_pages):
        pages = logged_in_pages
        with pytest.raises(AssertionError, match="No assignment row found"):
            pages.workspace_page.open_known_assignment("ZZZ_NO_ASSIGNMENT_EXISTS_999")
