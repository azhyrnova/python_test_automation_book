import pytest
from playwright.sync_api import sync_playwright
from utils.logger import setup_logger

# Hook to dynamically assign log files based on markers
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
    if 'ui' in item.keywords:  # Marked with @pytest.mark.ui
        log_file = "logs/ui_tests.log"
    elif 'api' in item.keywords:  # Marked with @pytest.mark.api
        log_file = "logs/api_tests.log"
    else:
        log_file = "logs/general_tests.log"  # Default log file

    # Set up the logger with the selected log file
    logger = setup_logger(item.name, log_file)
    
    # Assign the logger to the item so you can use it in tests
    item.logger = logger
    return None  # Allow the test to continue

# Define a pytest fixture to set up Playwright and browser instance
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False
        )
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context(
        viewport={"width": 1280, "height": 720}
        )
    page = context.new_page()
    yield page
    context.close()

#Generating screenshot on a test failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Get the outcome of the test
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")  # Get the page fixture
        if page:
            screenshot_path = f"screenshots/{item.name}.png"
            page.screenshot(path=screenshot_path)
            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html:
                # Attach screenshot to pytest-html report
                extra = getattr(report, "extra", [])
                extra.append(pytest_html.extras.image(screenshot_path))
                report.extra = extra