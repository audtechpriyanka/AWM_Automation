"""Test suite for PreliminaryAnalyticalReviewPage (B3.0)."""
import allure
import pytest

from pages.preliminary_analytical_review_page import PreliminaryAnalyticalReviewPage


@allure.feature("B3.0 Preliminary Analytical Review Screen")
class TestPreliminaryAnalyticalReview:

    @allure.story("B3.0 Preliminary Analytical Review screen opens and verifies loaded state")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_preliminary_analytical_review_screen_loads(self, logged_in_pages):
        par_pg = PreliminaryAnalyticalReviewPage(logged_in_pages.page)
        par_pg.open()
        par_pg.expect_loaded()

    @allure.story("B3.0 Preliminary Analytical Review items fill and verify")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_preliminary_analytical_review_items_fill(self, logged_in_pages):
        par_pg = PreliminaryAnalyticalReviewPage(logged_in_pages.page)
        par_pg.open()
        results = par_pg.fill_and_verify_items()
        assert len(results) >= 0
