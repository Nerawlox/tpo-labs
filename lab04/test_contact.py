import itertools

import pytest

from conftest import screenshot
from lab04.pages.contact_page import ContactPage

pytestmark = pytest.mark.ui


@pytest.mark.parametrize("name_ok,email_ok,message_ok", list(itertools.product([True, False], repeat=3)))
def test_required_fields_matrix(browser, base_url, name_ok, email_ok, message_ok):
    page = ContactPage(browser, base_url).load()
    page.submit("Иван" if name_ok else "", "student@example.com" if email_ok else "", "Учебная проверка формы" if message_ok else "")
    if all((name_ok, email_ok, message_ok)):
        assert page.success_message() == "Сообщение успешно принято"
        screenshot(browser, "lab04", "01_success")
    else:
        for field, valid, title in (("name", name_ok, "Имя"), ("email", email_ok, "Email"), ("message", message_ok, "Сообщение")):
            if not valid:
                assert page.error(field) == f"{title}: обязательное поле"
        assert not browser.find_element(*page.SUCCESS).is_displayed()
        screenshot(browser, "lab04", f"matrix_{int(name_ok)}{int(email_ok)}{int(message_ok)}")


@pytest.mark.parametrize("email", ["invalid", "a@b", "user @example.com"])
def test_invalid_email(browser, base_url, email):
    page = ContactPage(browser, base_url).load()
    page.submit("Иван", email, "Учебная проверка")
    assert page.error("email") == "Введите корректный email"
    assert not browser.find_element(*page.SUCCESS).is_displayed()
    screenshot(browser, "lab04", "02_invalid_email")


def test_whitespace_is_not_a_name(browser, base_url):
    page = ContactPage(browser, base_url).load()
    page.submit("   ", "student@example.com", "Проверка пробелов")
    assert page.error("name") == "Имя: обязательное поле"
    screenshot(browser, "lab04", "03_whitespace_name")
