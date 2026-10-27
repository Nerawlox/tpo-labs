from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def open(self, path):
        self.driver.get(self.base_url + path)
        return self

    def fill(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def visible_text(self, locator):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.wait.until(lambda _: element.text.strip() != "")
        return element.text
