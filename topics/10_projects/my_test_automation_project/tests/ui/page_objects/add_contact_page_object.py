from playwright.sync_api import Page

class AddContactPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name_field = page.locator("#firstName")
        self.last_name_field = page.locator("#lastName")
        self.email_field = page.locator("#email")
        self.submit_button = page.locator("#submit")
        
    def fill_in_new_contact_data(self, first_name: str, last_name: str, email: str) -> object:
        self.first_name_field.fill(first_name)
        self.last_name_field.fill(last_name)
        self.email_field.fill(email)
        
    def submit_data(self):
        self.submit_button.click() 