import os
import threading
from pathlib import Path

import pytest
from selenium import webdriver

from server import make_server

ROOT = Path(__file__).resolve().parent


@pytest.fixture(scope="session")
def base_url():
    with make_server() as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        yield f"http://127.0.0.1:{server.server_port}"
        server.shutdown()
        thread.join()


def create_browser():
    options = webdriver.ChromeOptions()
    if os.environ.get("HEADED") != "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1080")
    options.add_argument("--lang=ru")
    options.add_argument("--force-device-scale-factor=1")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver


@pytest.fixture
def browser():
    driver = create_browser()
    yield driver
    driver.quit()


def screenshot(driver, lab, name):
    folder = ROOT / lab / "screenshots"
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / f"{name}.png"
    driver.save_screenshot(str(target))
    return str(target.relative_to(ROOT))
