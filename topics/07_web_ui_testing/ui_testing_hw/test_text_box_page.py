import pytest
from text_box_page_object import TextBoxPage
from playwright.sync_api import sync_playwright

@pytest.fixture
def contact_data():
    return {
        "full_name": "Donald Duck",
        "email": "donald.duck@example.com",
        "current_address": "56 Main St",
        "permanent_address": "379 Apple Rd",
    }

@pytest.fixture
def wrong_contact_data():
    return {
        "full_name": "Donald Duck",
        "email": "donald.duck", #Invalid email
        "current_address": "56 Main St",
        "permanent_address": "379 Apple Rd",
    }


def test_user_can_fill_in_contact_details(page, contact_data):
    text_box_page = TextBoxPage(page)
    text_box_page.navigate("https://demoqa.com/text-box")
    text_box_page.fill_contact_data(
        full_name=contact_data["full_name"],
        email=contact_data["email"],
        current_address=contact_data["current_address"],
        permanent_address=contact_data["permanent_address"]
    )
    text_box_page.submit_data()

    assert text_box_page.output.is_visible(), "Output section is not visible after form submission."
    
    # Assert the output contains the expected details
    output_text = text_box_page.output.inner_text()
    assert contact_data["full_name"] in output_text, f"Full name '{contact_data['full_name']}' not found in output."
    assert contact_data["email"] in output_text, f"Email '{contact_data['email']}' not found in output."
    assert contact_data["current_address"] in output_text, f"Current address '{contact_data['current_address']}' not found in output."
    assert contact_data["permanent_address"] in output_text, f"Permanent address '{contact_data['permanent_address']}' not found in output."
    
def test_form_is_not_sent_if_email_is_incorrect(page, wrong_contact_data):
    text_box_page = TextBoxPage(page)
    text_box_page.navigate("https://demoqa.com/text-box")
    
    text_box_page.fill_contact_data(
        full_name=wrong_contact_data["full_name"],
        email=wrong_contact_data["email"],
        current_address=wrong_contact_data["current_address"],
        permanent_address=wrong_contact_data["permanent_address"]
    )
    text_box_page.submit_data()
    
    error_field = page.locator('//input[@id="userEmail" and contains(@class, "field-error")]')
    assert error_field.is_visible(), "The error state is not visible for the email field."
    
def test_simulating_fail_test(page, wrong_contact_data):
    text_box_page = TextBoxPage(page)
    text_box_page.navigate("https://demoqa.com/text-box")
    
    text_box_page.fill_contact_data(
        full_name=wrong_contact_data["full_name"],
        email="",
        current_address="",
        permanent_address=""
    )
    
    text_box_page.submit_data()
    # Always failing assertion
    assert 1 == 2, "This test is designed to fail for simulation purposes."    