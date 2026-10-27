import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import screenshot

pytestmark = pytest.mark.ui


def test_valid_login_and_logout(browser, base_url):
    browser.get(base_url + "/lab03/app/")
    browser.find_element(By.ID, "username").send_keys("student")
    browser.find_element(By.ID, "password").send_keys("Study123!")
    screenshot(browser, "lab03", "02_credentials")
    browser.find_element(By.ID, "login").click()
    logout = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "logout")))
    assert "Добро пожаловать, student!" in browser.find_element(By.ID, "dashboard").text
    screenshot(browser, "lab03", "03_successful_login")
    browser.refresh()
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "logout")))
    logout = browser.find_element(By.ID, "logout")
    logout.click()
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "login")))
    assert not browser.find_element(By.ID, "dashboard").is_displayed()
    screenshot(browser, "lab03", "04_logout")


def test_invalid_login(browser, base_url):
    browser.get(base_url + "/lab03/app/")
    browser.find_element(By.ID, "username").send_keys("student")
    browser.find_element(By.ID, "password").send_keys("wrong-password")
    browser.find_element(By.ID, "login").click()
    WebDriverWait(browser, 10).until(EC.text_to_be_present_in_element((By.ID, "login-error"), "Неверный логин или пароль"))
    assert not browser.find_element(By.ID, "dashboard").is_displayed()
    screenshot(browser, "lab03", "05_invalid_login")
