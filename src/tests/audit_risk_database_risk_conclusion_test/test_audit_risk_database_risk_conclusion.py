"""Test suite for AuditRiskDatabaseRiskConclusionPage (B8.0 riskconclusion)."""
import allure
import pytest

from pages.audit_risk_database_risk_conclusion_page import AuditRiskDatabaseRiskConclusionPage


@allure.feature("B8.0 Audit Risk Database Risk Conclusion")
class TestAuditRiskDatabaseRiskConclusion:

    @allure.story("Risk conclusion screen opens via riskconclusion route")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_risk_conclusion_screen_loads(self, logged_in_pages):
        pg = AuditRiskDatabaseRiskConclusionPage(logged_in_pages.page)
        pg.open()
        pg.expect_loaded()

    @allure.story("Risk cards expand and show detail fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_risk_conclusion_items_expand(self, logged_in_pages):
        pg = AuditRiskDatabaseRiskConclusionPage(logged_in_pages.page)
        pg.open()
        results = pg.fill_and_verify_items()
        assert len(results) >= 1
        assert all(v == "Pass" for v in results.values())
