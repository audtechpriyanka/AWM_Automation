"""
Client management tests — search + create (Basic Info validation).
"""
import allure
import pytest


KNOWN_CLIENT = "Apex Finserve Private Limited"


@allure.feature("Client Management")
class TestClient:

    @allure.story("Search client by name")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_search_client_by_name(self, logged_in_pages):
        pages = logged_in_pages
        pages.client_page.open_search()
        pages.client_page.search_by_name(KNOWN_CLIENT)
        pages.client_page.expect_row_containing(KNOWN_CLIENT)

    @allure.story("Search with unknown name")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.negative
    def test_search_client_no_results(self, logged_in_pages):
        pages = logged_in_pages
        pages.client_page.open_search()
        before = pages.client_page.row_count()
        pages.client_page.search_by_name("ZZZ_NO_SUCH_CLIENT_99999")
        pages.page.wait_for_timeout(1500)
        after = pages.client_page.row_count()
        # Either fewer rows than the unfiltered list, or an empty-state message.
        body = pages.page.locator("body").inner_text().lower()
        assert after < before or after == 0 or "no " in body

    @allure.story("Search form fields visible")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_search_form_fields_present(self, logged_in_pages):
        pages = logged_in_pages
        pages.client_page.open_search()
        pages.client_page.expect_visible(pages.client_page.search_name_field())
        pages.client_page.expect_visible(pages.client_page.search_email_field())
        pages.client_page.expect_visible(pages.client_page.search_contact_field())
        pages.client_page.expect_visible(pages.client_page.search_button())

    @allure.story("Create client — Basic Info step loads")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_create_client_form_loads(self, logged_in_pages):
        pages = logged_in_pages
        pages.client_page.open_create()
        pages.client_page.expect_visible(pages.client_page.client_name_field())
        pages.client_page.expect_visible(pages.client_page.next_button())
        pages.client_page.expect_visible(pages.client_page.org_type_select())

    @allure.story("Create client — NEXT blocked when required empty")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.negative
    def test_create_client_next_requires_fields(self, logged_in_pages):
        pages = logged_in_pages
        pages.client_page.open_create()
        pages.client_page.click_next()
        # Assumption: wizard stays on Basic Info and/or shows mat-error when required fields empty.
        pages.client_page.expect_visible(pages.client_page.step_basic_info())
        pages.client_page.expect_visible(pages.client_page.client_name_field())

    @allure.story("Create client — name accepts long boundary value")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_create_client_name_boundary(self, logged_in_pages):
        pages = logged_in_pages
        pages.client_page.open_create()
        long_name = "AutoQA " + ("X" * 80)
        pages.client_page.fill_basic_info(long_name)
        # Field should retain the value (boundary: long but plausible name).
        assert long_name[:20] in pages.client_page.client_name_field().input_value()
