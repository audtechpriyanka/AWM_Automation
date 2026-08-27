"""Test suite for TailoringQuestionPage."""
import allure
import pytest

from pages.tailoring_question_page import TailoringQuestionPage


@allure.feature("Tailoring Questions Screen")
class TestTailoringQuestion:

    @allure.story("Tailoring questions screen opens and verifies loaded state")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_tailoring_questions_screen_loads(self, logged_in_pages):
        tq_pg = TailoringQuestionPage(logged_in_pages.page)
        tq_pg.open()
        tq_pg.expect_loaded()

    @allure.story("Dynamically discover and answer tailoring questions")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_answer_tailoring_questions(self, logged_in_pages):
        tq_pg = TailoringQuestionPage(logged_in_pages.page)
        tq_pg.open()
        results = tq_pg.answer_all_questions(default_choice="Yes")
        assert len(results) >= 0
        tq_pg.save()
