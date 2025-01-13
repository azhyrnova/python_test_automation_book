import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    # Retrieve values from environment variables or fallback to defaults
    TOKEN = os.getenv("TOKEN")
    TEST_EMAIL = "test2@fake.com"
    TEST_PASSWORD = os.getenv("TEST_PASSWORD")
    BASE_URL = "https://thinking-tester-contact-list.herokuapp.com"
    LOGIN_URL = f"{BASE_URL}/users/login"
    LOGOUT_URL = f"{BASE_URL}/users/logout"
    CONTACT_LIST_URL = f"{BASE_URL}/contacts"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    USE_API_DIR = bool(os.getenv("USE_API_DIR", True))