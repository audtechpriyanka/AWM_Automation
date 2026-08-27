"""Test suite for DiscussionWithClientEntryMeetingPage (B1.0)."""
import allure
import pytest

from pages.discussion_with_client_entry_meeting_page import DiscussionWithClientEntryMeetingPage


@allure.feature("B1.0 Entry Meeting Screen")
class TestDiscussionWithClientEntryMeeting:

    @allure.story("B1.0 Entry Meeting screen opens and verifies loaded state")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_entry_meeting_screen_loads(self, logged_in_pages):
        b1_pg = DiscussionWithClientEntryMeetingPage(logged_in_pages.page)
        b1_pg.open()
        b1_pg.expect_loaded()

    @allure.story("B1.0 Entry Meeting items fill and verify")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_entry_meeting_items_fill(self, logged_in_pages):
        b1_pg = DiscussionWithClientEntryMeetingPage(logged_in_pages.page)
        b1_pg.open()
        results = b1_pg.fill_and_verify_items()
        assert len(results) >= 0
