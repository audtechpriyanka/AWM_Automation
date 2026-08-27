"""Test suite for TrialBalancePage (#/assignment/.../importtb)."""
import allure
import pytest

from pages.trial_balance_page import TrialBalancePage


@allure.feature("Trial Balance Screen")
class TestTrialBalance:

    @allure.story("Trial balance screen opens and verifies loaded state")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_trial_balance_screen_loads(self, logged_in_pages):
        tb_pg = TrialBalancePage(logged_in_pages.page)
        tb_pg.open()
        tb_pg.expect_loaded()

    @allure.story("Trial balance file input and action controls are present")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_trial_balance_controls_present(self, logged_in_pages):
        tb_pg = TrialBalancePage(logged_in_pages.page)
        tb_pg.open()
        assert tb_pg.file_input().count() > 0 or tb_pg.choose_file_label().count() > 0
        tb_pg.expect_visible(tb_pg.preview_button())
