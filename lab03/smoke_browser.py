"""Open the own login stand and close Chrome using Selenium."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from conftest import create_browser, screenshot

if __name__ == "__main__":
    driver = create_browser()
    try:
        driver.get("http://127.0.0.1:8765/lab03/app/")
        print(f"Opened page: {driver.title}")
        screenshot(driver, "lab03", "01_login_page")
    finally:
        driver.quit()
        print("Browser closed")
