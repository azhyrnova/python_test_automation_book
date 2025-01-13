from playwright.sync_api import Page

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.email_field = page.locator("#email") 
        self.password_field = page.locator("#password")
        self.submit_button = page.locator("#submit")
        self.signup_button = page.locator("#signup")
        self.error = page.locator("#error")
        
    def navigate(self, url: str):
        self.page.goto(url)
        
    def fill_in_login_data(self, email: str, password: str) -> object:
        self.email_field.fill(email)
        self.password_field.fill(password)
        
    def submit_data(self):
        self.submit_button.click()