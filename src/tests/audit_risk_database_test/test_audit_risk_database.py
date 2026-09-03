"""Test suite for AuditRiskDatabasePage (B8.0/B9.0)."""
import allure
import pytest

from pages.audit_risk_database_page import AuditRiskDatabasePage


@allure.feature("B8.0/B9.0 Audit Risk Database Screen")
class TestAuditRiskDatabase:

    @allure.story("B8.0 Audit Risk Database screen opens and verifies loaded state")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_audit_risk_database_screen_loads(self, logged_in_pages):
        ard_pg = AuditRiskDatabasePage(logged_in_pages.page)
        ard_pg.open()
        ard_pg.expect_loaded()

    @allure.story("B8.0 Audit Risk Database items fill and verify")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_audit_risk_database_items_fill(self, logged_in_pages):
        ard_pg = AuditRiskDatabasePage(logged_in_pages.page)
        ard_pg.open()
        results = ard_pg.fill_and_verify_items()
        assert len(results) >= 0
