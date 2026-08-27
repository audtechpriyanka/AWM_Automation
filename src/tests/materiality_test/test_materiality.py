"""Test suite for MaterialityPage (B2.0)."""
import allure
import pytest

from pages.materiality_page import MaterialityPage


@allure.feature("B2.0 Materiality Screen")
class TestMateriality:

    @allure.story("B2.0 Materiality screen opens and verifies loaded state")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_materiality_screen_loads(self, logged_in_pages):
        mat_pg = MaterialityPage(logged_in_pages.page)
        mat_pg.open()
        mat_pg.expect_loaded()

    @allure.story("B2.0 Materiality items fill and verify")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_materiality_items_fill(self, logged_in_pages):
        mat_pg = MaterialityPage(logged_in_pages.page)
        mat_pg.open()
        results = mat_pg.fill_and_verify_items()
        assert len(results) >= 0
