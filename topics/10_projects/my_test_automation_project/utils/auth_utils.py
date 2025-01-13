import requests
import logging
from config.config import Config

logger = logging.getLogger(__name__)

LOGIN_URL = Config.LOGIN_URL

def login_and_get_token(login_data):
    """
    Logs in using the provided credentials and returns the authentication token.

    Args:
        login_data (dict): A dictionary with keys "email" and "password".

    Returns:
        str: The authentication token.

    Raises:
        Exception: If the login fails or the response cannot be parsed.
    """
    payload = {
        "email": login_data["email"],
        "password": login_data["password"]
    }
    logger.debug("Attempting login...")
    #logger.debug(f"Attempting login with payload: {payload}")
    
    # Perform the login request
    response = requests.post(LOGIN_URL, json=payload)
    
    # Ensure login is successful
    if response.status_code != 200:
        logger.error(f"Login failed: {response.status_code}, {response.text}")
        raise Exception(f"Login failed: {response.status_code}, {response.text}")
    
    # Extract the token from the response
    try:
        token = response.json().get("token")
        if not token:
            logger.error("Token not found in login response.")
            raise Exception("Token not found in login response.")
        #logger.debug(f"Login successful. Token: {token}")
        return token
    except ValueError as e:
        logger.error(f"Failed to parse login response as JSON. Response: {response.text}")
        raise e
