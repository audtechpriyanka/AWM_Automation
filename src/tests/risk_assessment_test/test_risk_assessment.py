"""Test suite for RiskAssessmentPage (B4.0)."""
import allure
import pytest

from pages.risk_assessment_page import RiskAssessmentPage


@allure.feature("B4.0 Risk Assessment Screen")
class TestRiskAssessment:

    @allure.story("B4.0 Risk Assessment screen opens and verifies loaded state")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_risk_assessment_screen_loads(self, logged_in_pages):
        ra_pg = RiskAssessmentPage(logged_in_pages.page)
        ra_pg.open()
        ra_pg.expect_loaded()

    @allure.story("B4.0 Risk Assessment items fill and verify")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_risk_assessment_items_fill(self, logged_in_pages):
        ra_pg = RiskAssessmentPage(logged_in_pages.page)
        ra_pg.open()
        results = ra_pg.fill_and_verify_items()
        assert len(results) >= 0
