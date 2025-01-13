import pytest
import requests

from config.config import Config
from utils.logger import setup_logger
from utils.auth_utils import login_and_get_token

logger = setup_logger("api_test_logger", log_file="logs/api_tests.log")
logger.info("Logger initialized successfully!")
logger.info("This is an info message.")
logger.debug("This is a debug message.")

LOGIN_URL = Config.LOGIN_URL
LOGOUT_URL = Config.LOGOUT_URL
CONTACT_LIST_URL = Config.CONTACT_LIST_URL
BEARER_TOKEN = Config.TOKEN
headers_without_auth = {"Content-Type": "application/json"}

@pytest.fixture
def login_data():
    return {
        "email": Config.TEST_EMAIL,
        "password": Config.TEST_PASSWORD
}
    
@pytest.fixture(scope="class")
def headers():
        return {"Content-Type": "application/json"}
    
@pytest.fixture(scope="class")
def headers_with_auth():
        return {"Authorization": "Bearer "+ BEARER_TOKEN}

@pytest.mark.api
def test_login_user(headers, login_data):
    logger.debug("Starting log in user test")
    payload = {
        "email": login_data["email"],
        "password": login_data["password"]
    }
    response = requests.post(LOGIN_URL, headers=headers, json=payload)
    #Log the response for debugging
    logger.debug(f"Response Status Code: {response.status_code}")
    logger.debug(f"Response Body: {response.text}")
    
    if response.status_code != 200:
         logger.error(f"Failed to login. Status code: {response.status_code}, Response: {response.text}")
         logger.debug(f"Response: {response.text}")
         response.raise_for_status()  # This will raise an exception and stop the test
    try:
         response_data = response.json()
    except ValueError as e:
         logger.error(f"Failed to parse JSON. Response: {response.text}")
         raise e  # Re-raise the exception for the test to fail
    assert response.status_code == 200
    
    logger.info("Checking that it is possible to extract token from response")
    try:
        response_data = response.json()
        logger.debug(f"Response JSON: {response_data}")
        token = response_data.get("token")
        assert token is not None, "Token not found in the response."
    except ValueError as e:
        logger.error(f"Failed to parse JSON response. Error: {e}")
        raise  

@pytest.mark.api 
def test_logout_user(headers, headers_with_auth, login_data):
    logger.debug("Starting log out user test")
    # Log in and get the token
    token = login_and_get_token(login_data)
       
    logger.info("Trying to log out the user")
    headers_with_auth = {"Authorization": f"Bearer {token}"}
    logout_response = requests.post(LOGOUT_URL, headers=headers_with_auth)
    
    # Log the logout response
    logger.debug(f"Logout Response Status Code: {logout_response.status_code}")
    logger.debug(f"Logout Response Body: {logout_response.text}")
        
    assert logout_response.status_code == 200, f"Logout failed: {logout_response.text}"