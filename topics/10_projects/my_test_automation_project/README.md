# Contact List App Automation

## Overview

The **Contact List App Automation** project provides automated tests for the Contact List application using **Playwright** for Web UI testing and **pytest** for API testing. The project implements a modular Test Automation Framework with separate suites for UI and API tests. It supports different markers and cleanup functionality to facilitate easy test execution and management.

## Project Structure

### 1. **Web UI Test Suite**
The UI test suite is based on the **Playwright** test automation tool. It uses the Page Object Model (POM) design pattern to interact with the application. The suite includes the following page objects and test files:

- **Page Objects**:
  - `HomePage`
  - `ContactListPage`
  - `AddContactPage`

- **Test Files**:
  - `test_contact_list_page.py`
  - `test_home_page.py`

#### To Run UI Tests:

You can execute the UI tests using **pytest** with markers:

- To run all UI tests:
  ```bash
  pytest -m "ui"

- To run tests based on the scope marker (e.g., smoke, regression)
  ```bash
  pytest -m "smoke"
  pytest -m "regression"

### **2. API Test Suite**
The API test suite is designed for testing the API endpoints of the Contact List application. The suite includes two main files:

- **Test Files**:
  - `test_users.py` :Contains POST tests for Login and Logout functions.
  - `test_contacts.py`: Contains tests for creating, updating, and deleting contacts.

The API documentation can be found here: https://documenter.getpostman.com/view/4012288/TzK2bEa8

- To Run API Tests:
You can execute the API tests using pytest with markers:

- To run all API tests:
  ```bash
  pytest -m "api"
-  To run tests based on the scope marker (e.g., smoke, regression):
  ```bash
  pytest -m "smoke"
  pytest -m "regression"
-  To run test and generate HTML report:
  ```bash
  pytest -m "smoke" --html=report.html --self-contained-html
  pytest -m "regression" --html=report.html --self-contained-html

### **3. Cleanup Tests**
There is a special "cleanup" marker designed for cleaning up data created during UI tests. Some data cannot be deleted directly via the UI, and these tests ensure that any leftover data is cleaned up.

To run the cleanup tests, first run the UI tests:
pytest -m "ui"

Then execute the cleanup tests:
pytest -m "cleanup"

### **4. Markers**
The project uses pytest markers to categorize and manage tests effectively. The available markers are:

ui: Marks UI tests.
api: Marks API tests.
smoke: Marks smoke tests.
regression: Marks regression tests.
cleanup: Marks cleanup tests to delete data created by UI tests.
You can configure and modify these markers in the pytest.ini file.

### Installation
Prerequisites
Python 3.x
pip (Python package manager)
TBC

### Logging and Reports
The project uses logging to capture detailed information during the execution of tests. Logs are stored in the logs/ directory and can be reviewed for debugging and analysis.