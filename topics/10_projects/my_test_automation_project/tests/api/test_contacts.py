import pytest
import requests

from config.config import Config
from utils.auth_utils import login_and_get_token
from utils.logger import setup_logger

logger = setup_logger("api_test_logger", log_file="logs/api_tests.log")
logger.info("This is an info message.")
logger.debug("This is a debug message.")

LOGIN_URL = Config.LOGIN_URL
CONTACT_LIST_URL = Config.CONTACT_LIST_URL
BEARER_TOKEN = Config.TOKEN

@pytest.fixture
def login_data():
    return {
        "email": Config.TEST_EMAIL,
        "password": Config.TEST_PASSWORD
    }

@pytest.fixture
def contact_data(scope="class"):
    return {
        "firstName": "Jack",
        "lastName": "Black",
        "birthdate": "1970-01-01",
        "email": "jblack@fake.com",
        "phone": "8005555555",
        "street1": "1 Main St.",
        "street2": "Apartment A",
        "city": "Anytown",
        "stateProvince": "KS",
        "postalCode": "12345",
        "country": "UK"
    }
    
@pytest.fixture
def data_to_delete(scope="class"):
    return {
        "firstName": "Jeanna",
        "lastName": "Smith",
        "email": "jsmith@fake.com"
    }
    
@pytest.fixture(scope="class")
def headers():
        return {"Content-Type": "application/json"}
    
@pytest.fixture(scope="class")
def headers_with_auth():
        return {"Authorization": "Bearer "+ BEARER_TOKEN}   
    
@pytest.mark.api
@pytest.mark.smoke      
def test_get_contact_list(headers_with_auth, login_data):
    """
    Checking GET 
    Get Contact List request: return a list of all available contacts
    """
    logger.debug("Starting get contact list test")
    
    # Log in and get the token
    token = login_and_get_token(login_data)
    headers_with_auth = {"Authorization": f"Bearer {token}"}
    
    # Fetch the contact list
    response = requests.get(CONTACT_LIST_URL, headers=headers_with_auth)
    
    # Log the contact list response
    logger.debug(f"Contact List Response Status Code: {response.status_code}")
    logger.debug(f"Contact List Response Body: {response.text}")
    
    # Ensure the request was successful
    assert response.status_code == 200, f"Failed to fetch contact list: {response.text}"
    
    # Parse and log the contact list
    try:
        contact_list = response.json()
        logger.debug(f"Contact List: {contact_list}")
        return contact_list
    except ValueError as e:
        logger.error(f"Failed to parse contact list response as JSON. Response: {response.text}")
        raise e

@pytest.mark.api
@pytest.mark.regression
def test_add_contact(headers_with_auth, login_data, contact_data):
    """
    Checking POST: Add Contact request adds a new contact to the list.
    """
    logger.debug("Starting add contact test")
    
    # Log in and get the token
    token = login_and_get_token(login_data)
    headers_with_auth = {"Authorization": f"Bearer {token}"} 
    
    # Payload for the new contact
    payload = {
        "firstName": contact_data["firstName"],
        "lastName": contact_data["lastName"],
        "birthdate": contact_data["birthdate"],
        "email": contact_data["email"],
        "phone": contact_data["phone"],
        "street1": contact_data["street1"],
        "street2": contact_data["street2"],
        "city": contact_data["city"],
        "stateProvince": contact_data["stateProvince"],
        "postalCode": contact_data["postalCode"],
        "country": contact_data["country"]
    }
    
    # Add new contact to the contact list
    response = requests.post(CONTACT_LIST_URL, headers=headers_with_auth, json=payload)
    logger.debug(f"Add Contact Response: {response.status_code}, {response.text}")

    # Assert that the contact was successfully added
    assert response.status_code == 201, f"Failed to add contact. Status code: {response.status_code}, Response: {response.text}"

    # Verify the contact appears in the list
    contact_list_response = requests.get(CONTACT_LIST_URL, headers=headers_with_auth)
    assert contact_list_response.status_code == 200, "Failed to retrieve contact list."
    contact = next(
        (contact for contact in contact_list_response.json() if contact["email"] == payload["email"]),
        None
    )
    assert contact, f"Contact with email {payload['email']} not found in the contact list."
    contact_id = contact["_id"]
    
    # Cleanup: Delete the created contact
    delete_response = requests.delete(f"{CONTACT_LIST_URL}/{contact_id}", headers=headers_with_auth)
    logger.debug(f"Delete Contact Response: {delete_response.status_code}, {delete_response.text}")
    assert delete_response.status_code == 200, "Cleanup failed: Unable to delete the contact."

@pytest.mark.api
@pytest.mark.regression
def test_update_contact(headers_with_auth, login_data, contact_data):
    """
    Checking POST: Update existing Contact.
    """
    logger.debug("Starting update contact test")
    # Log in and get the token
    token = login_and_get_token(login_data)
    headers_with_auth = {"Authorization": f"Bearer {token}"}
    
    # Payload for the new contact, precondition for an update
    payload = {
        "firstName": contact_data["firstName"],
        "lastName": contact_data["lastName"],
        "birthdate": contact_data["birthdate"],
        "email": contact_data["email"],
        "phone": contact_data["phone"],
        "street1": contact_data["street1"],
        "street2": contact_data["street2"],
        "city": contact_data["city"],
        "stateProvince": contact_data["stateProvince"],
        "postalCode": contact_data["postalCode"],
        "country": contact_data["country"]
    }
    
    # Add new contact to the contact list
    response = requests.post(CONTACT_LIST_URL, headers=headers_with_auth, json=payload)
    logger.debug(f"Add Contact Response: {response.status_code}, {response.text}")

    # Assert that the contact was successfully added
    assert response.status_code == 201, f"Failed to add contact. Status code: {response.status_code}, Response: {response.text}"
    
    # Payload for the contact update
    updated_contact_data = {
        "firstName": "Albert",  
        "phone": "8006666666"        
    }
    
    # Fetch the existing contact first (to get its ID for updating)
    contact_list_response = requests.get(CONTACT_LIST_URL, headers=headers_with_auth)
    assert contact_list_response.status_code == 200, "Failed to retrieve contact list."
    
    # Find the contact that we want to update (using email or other identifier)
    contact = next(
        (contact for contact in contact_list_response.json() if contact["email"] == contact_data["email"]),
        None
    )
    assert contact, f"Contact with email {contact_data['email']} not found in the contact list."
    contact_id = contact["_id"]
    
    # Send the PATCH request to update the contact
    update_response = requests.patch(f"{CONTACT_LIST_URL}/{contact_id}", headers=headers_with_auth, json=updated_contact_data)
    logger.debug(f"Update Contact Response: {update_response.status_code}, {update_response.text}")

    # Assert that the contact was successfully updated
    assert update_response.status_code == 200, f"Failed to update contact. Status code: {update_response.status_code}, Response: {update_response.text}"

    # Verify that the contact was updated correctly
    updated_contact = update_response.json()
    assert updated_contact["firstName"] == updated_contact_data["firstName"], f"First name was not updated."
    assert updated_contact["phone"] == updated_contact_data["phone"], f"Phone number was not updated." 
    
    # Cleanup: Delete the created contact
    delete_response = requests.delete(f"{CONTACT_LIST_URL}/{contact_id}", headers=headers_with_auth)
    logger.debug(f"Delete Contact Response: {delete_response.status_code}, {delete_response.text}")
    assert delete_response.status_code == 200, "Cleanup failed: Unable to delete the contact."

@pytest.mark.api 
@pytest.mark.regression   
def test_delete_contact(headers_with_auth, login_data, contact_data):
    """
    Checking DELETE: Remove a newly created contact from the contact list.
    """
    logger.debug("Starting delete contact test")
    
    # Log in and get the token
    token = login_and_get_token(login_data)
    headers_with_auth = {"Authorization": f"Bearer {token}"}
    
    # Payload for the new contact    
    payload = {
        "firstName": contact_data["firstName"],
        "lastName": contact_data["lastName"],
        "birthdate": contact_data["birthdate"],
        "email": contact_data["email"],
        "phone": contact_data["phone"],
        "street1": contact_data["street1"],
        "street2": contact_data["street2"],
        "city": contact_data["city"],
        "stateProvince": contact_data["stateProvince"],
        "postalCode": contact_data["postalCode"],
        "country": contact_data["country"]
    }
    
    # Add new contact
    response = requests.post(CONTACT_LIST_URL, headers=headers_with_auth, json=payload)
    logger.debug(f"Add Contact Response: {response.status_code}, {response.text}")
    assert response.status_code == 201, "Failed to add contact before deletion."

    # Get the contact ID
    contact_list_response = requests.get(CONTACT_LIST_URL, headers=headers_with_auth)
    assert contact_list_response.status_code == 200, "Failed to retrieve contact list."
    
    # Find the newly created contact in the response
    contact_list = contact_list_response.json()
    contact = next(
        (c for c in contact_list if c.get("email") == payload["email"]),
        None
    )
    assert contact, f"Contact with email {payload['email']} not found before deletion."
    contact_id = contact["_id"]

    # Delete the contact
    delete_response = requests.delete(f"{CONTACT_LIST_URL}/{contact_id}", headers=headers_with_auth)
    logger.debug(f"Delete Contact Response: {delete_response.status_code}, {delete_response.text}")
    assert delete_response.status_code == 200, f"Failed to delete contact. Status code: {delete_response.status_code}"

    # Verify the contact no longer exists
    contact_list_response = requests.get(CONTACT_LIST_URL, headers=headers_with_auth)
    assert contact_list_response.status_code == 200, "Failed to retrieve contact list after deletion."
    contact_list = contact_list_response.json()
    assert not any(
        c for c in contact_list if c.get("email") == payload["email"]
    ), f"Contact with email {payload['email']} still exists after deletion."
    
@pytest.mark.cleanup
@pytest.mark.api
#@pytest.mark.dependency(depends=[test_contact_list_page.test_user_can_add_a_new_contact])
def test_delete_as_cleanup_for_ui_tests(headers_with_auth, login_data, data_to_delete):
    """
    Checking DELETE: Remove a contact to perform a clean-up after UI test execution.
    """
    logger.debug("Starting delete as cleanup for UI contact test")
    
    # Log in and get the token
    token = login_and_get_token(login_data)
    headers_with_auth = {"Authorization": f"Bearer {token}"}
      
    # Get the contact ID
    contact_list_response = requests.get(CONTACT_LIST_URL, headers=headers_with_auth)
    assert contact_list_response.status_code == 200, "Failed to retrieve contact list."
    
    # Find the newly created contact in the response
    contact_list = contact_list_response.json()
    contact = next(
        (c for c in contact_list if c.get("email") == data_to_delete["email"]),
        None
    )
    if not contact:
        logger.info(f"Contact with email {data_to_delete['email']} not found. Skipping cleanup.")
        return  # If contact is not found, skip the cleanup.
    contact_id = contact["_id"]

    
    delete_response = requests.delete(f"{CONTACT_LIST_URL}/{contact_id}", headers=headers_with_auth)
    logger.debug(f"Delete Contact Response: {delete_response.status_code}, {delete_response.text}")
    assert delete_response.status_code == 200, "Cleanup failed: Unable to delete the contact."