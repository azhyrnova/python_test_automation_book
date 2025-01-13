import pytest
from page_objects.home_page_object import HomePage
from page_objects.contact_list_page_object import ContactListPage
from page_objects.add_contact_page_object import AddContactPage
from playwright.sync_api import sync_playwright
from utils.logger import setup_logger
from config.config import Config
import requests

logger = setup_logger("ui_test_logger", log_file="logs/ui_tests.log")

@pytest.fixture
def login_data():
    return {
        "email": Config.TEST_EMAIL,
        "password": Config.TEST_PASSWORD
    }
    
@pytest.fixture
def new_contact_data():
    return {
        "first_name": "Jeanna",
        "last_name": "Smith",
        "email": "jsmith@fake.com"
    }

@pytest.mark.ui 
@pytest.mark.smoke
@pytest.mark.dependency()  
def test_user_can_add_a_new_contact(page, login_data, new_contact_data):
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
    contact_page.add_contact_button.click()
    
    add_new_contact_page = AddContactPage(page)
    add_new_contact_page.fill_in_new_contact_data(
        first_name=new_contact_data["first_name"],
        last_name=new_contact_data["last_name"],
        email = new_contact_data["email"]
    )
    add_new_contact_page.submit_data()
    #page.wait_for_load_state("domcontentloaded")
    
    contact_page.contacts_table.wait_for(state="visible")
    contact_data_as_string = " ".join([new_contact_data["first_name"], new_contact_data["last_name"]])
    
    # Assert that the new contact is in the table
    contact_locator = f"//*[@id='myTable']/tr/td[text()='{contact_data_as_string}']"
    locator_element = page.locator(contact_locator)

    assert locator_element.is_visible(), f"New contact '{contact_data_as_string}' not found in the contact list."
    
    logger.info(f"Contact '{contact_data_as_string}' successfully added to the contact list.")