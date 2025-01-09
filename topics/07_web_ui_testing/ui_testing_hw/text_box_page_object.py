from playwright.sync_api import Page

class TextBoxPage:
    # Initialize page and selectors
    def __init__(self, page: Page):
        self.page = page
        self.full_name_field = page.locator("#userName")
        self.email_field = page.locator("#userEmail")
        self.current_address_field = page.locator("#currentAddress")
        self.permanent_address_field = page.locator("#permanentAddress")
        self.submit_button = page.locator("#submit")
        self.output = page.locator("#output")
        
    def navigate(self, url: str):
        self.page.goto(url)
        
    def fill_contact_data(self, full_name: str, email: str, current_address: str, permanent_address: str):
        self.full_name_field.fill(full_name)
        self.email_field.fill(email)
        self.current_address_field.fill(current_address)
        self.permanent_address_field.fill(permanent_address)          

    def submit_data(self):
        self.submit_button.click()