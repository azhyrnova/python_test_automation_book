from playwright.sync_api import Page

class ContactListPage:
    def __init__(self, page: Page):
        self.page = page
        self.title_element = page.locator("header > h1")
        self.logout_button = page.locator("#logout") 
        self.add_contact_button = page.locator("#add-contact")
        self.contacts_table = page.locator("#myTable")
        
    def is_add_new_contact_button_visible(self):
        return self.add_contact_button.is_visible()
        
    def is_logout_button_visible(self):
        return self.logout_button.is_visible()
        
    def navigate(self, url: str):
        self.page.goto(url)        
        
    def logout(self) -> object:
        self.logout_button.click()