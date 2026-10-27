"""Capture browser views of real saved test output without editing the images."""
import sys
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from conftest import ROOT, create_browser, screenshot

if __name__ == '__main__':
    driver=create_browser()
    try:
        for lab in ['lab03','lab04','lab05','lab06']:
            driver.get(f'http://127.0.0.1:8765/{lab}/results/test-run.html')
            WebDriverWait(driver,20).until(lambda d:'passed' in d.find_element(By.TAG_NAME,'body').text.lower())
            screenshot(driver,lab,'90_pytest_results')
        driver.get('http://127.0.0.1:8765/lab05/results/postman-run.html')
        WebDriverWait(driver,20).until(lambda d:len(d.find_element(By.TAG_NAME,'body').text)>100)
        screenshot(driver,'lab05','91_postman_collection_run')
        driver.get('http://127.0.0.1:8765/lab05/results/get_users_1.json')
        screenshot(driver,'lab05','92_get_response')
        for profile in ['10vus-30s','50vus-10s']:
            driver.get(f'http://127.0.0.1:8765/lab08/results/{profile}-console.txt')
            driver.execute_script('document.body.style.fontSize="17px"; document.body.style.lineHeight="1.45"; window.scrollTo(0,document.body.scrollHeight)')
            screenshot(driver,'lab08',profile)
        if (ROOT/'lab07/results/mobile-checks.json').exists():
            driver.get('http://127.0.0.1:8765/lab07/results/appium-console.txt')
            driver.execute_script('document.querySelector("pre").style.whiteSpace="pre-wrap"; document.body.style.fontSize="17px"; document.body.style.lineHeight="1.5"')
            screenshot(driver,'lab07','90_appium_results')
    finally:driver.quit()
