from selenium.webdriver.common.by import By
from .base_page import BasePage


class ContactPage(BasePage):
    NAME = (By.ID, "name")
    EMAIL = (By.ID, "email")
    MESSAGE = (By.ID, "message")
    SEND = (By.ID, "send")
    SUCCESS = (By.ID, "success")

    def load(self):
        return self.open("/lab04/app/")

    def submit(self, name, email, message):
        self.fill(self.NAME, name)
        self.fill(self.EMAIL, email)
        self.fill(self.MESSAGE, message)
        self.click(self.SEND)

    def error(self, field):
        return self.visible_text((By.ID, field + "-error"))

    def success_message(self):
        return self.visible_text(self.SUCCESS)
