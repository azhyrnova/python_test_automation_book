import pytest
from page_objects.home_page_object import HomePage
from page_objects.contact_list_page_object import ContactListPage
from playwright.sync_api import sync_playwright
from utils.logger import setup_logger
from config.config import Config

logger = setup_logger(__name__, log_file="logs/ui_tests.log")

@pytest.fixture
def login_data():
    return {
        "email": Config.TEST_EMAIL,
        "password": Config.TEST_PASSWORD
    }

@pytest.fixture    
def wrong_login_data():
    return {
        "email": "fakelogin@fake.com",
        "password": "1234"
    }

@pytest.mark.ui
@pytest.mark.smoke
def test_user_can_login_with_correct_credentials(page, login_data):
    logger.debug("Starting UI login test")
    home_page = HomePage(page)
    home_page.navigate("https://thinking-tester-contact-list.herokuapp.com")
    
    home_page.fill_in_login_data(
        email = login_data["email"],
        password = login_data["password"]        
    )
    home_page.submit_data()
    page.wait_for_load_state("domcontentloaded")

    contact_page = ContactListPage(page)
    contact_page.add_contact_button.wait_for(state="visible")
    assert contact_page.is_logout_button_visible(), "Logout button is not visible, so login was not successful"
    assert contact_page.is_add_new_contact_button_visible(), "Add new contact button is not visible, so login was not successful"
    logger.info("Test passed.")
    
@pytest.mark.ui
def test_user_cannot_login_with_wrong_credentials(page, wrong_login_data):
    logger.debug("Starting UI login with wrong credentials test")
    home_page = HomePage(page)
    home_page.navigate("https://thinking-tester-contact-list.herokuapp.com")
    
    home_page.fill_in_login_data(
        email = wrong_login_data["email"],
        password = wrong_login_data["password"]        
    )
    
    home_page.submit_data()
    home_page.error.wait_for(state="visible")
    
    assert home_page.error.is_visible()
    error_message = home_page.error.text_content()
    assert error_message == "Incorrect username or password", f"Unexpected error message: {error_message}"
    logger.info("Test passed.")
