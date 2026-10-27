"""Replay documented UI cases and preserve actual values and browser screenshots."""
import json
import platform
import sys
from datetime import datetime
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from conftest import ROOT, create_browser, screenshot


def write_results(lab, driver, cases):
    folder = ROOT / lab / "results"
    folder.mkdir(parents=True, exist_ok=True)
    data = {"executed_at": datetime.now().astimezone().isoformat(),
            "environment": {"os": platform.platform(), "browser": driver.capabilities["browserName"], "browser_version": driver.capabilities["browserVersion"], "url": driver.current_url},
            "method": "UI case replay; Selenium performs input and captures unedited browser screenshots", "cases": cases}
    (folder / "ui-checks.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = ["# Фактические результаты UI-проверок", "", f"Дата: {data['executed_at']}", f"Окружение: {data['environment']}", "", "Пошаговое воспроизведение сценариев через браузер. Ввод и снимки выполнены Selenium; это не заявление о ручном прогоне человеком.", "", "| ID | Ожидалось | Получено | Статус | Скриншот |", "|---|---|---|---|---|"]
    for case in cases:
        rows.append(f"| {case['id']} | {case['expected']} | {case['actual']} | {case['status']} | {case['screenshot']} |")
    (folder / "ui-checks.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"{lab}: {sum(c['status']=='PASS' for c in cases)} PASS, {sum(c['status']=='FAIL' for c in cases)} FAIL")


def calculator_cases(driver, url):
    driver.get(url + "/lab01/app/")
    cases = []
    data = [
        ("TC01", "2", "3", "add", "5"), ("TC02", "7", "10", "subtract", "-3"),
        ("TC03", "-3", "4", "multiply", "-12"), ("TC04", "7", "2", "divide", "3.5"),
        ("TC05", "0,1", "0,2", "add", "0.3"), ("TC06", "0", "5", "multiply", "0"),
        ("TC07", "9", "0", "divide", "Деление на ноль невозможно"),
        ("TC08", "", "5", "add", "Введите два корректных числа"),
        ("TC09", "abc", "2", "add", "Введите два корректных числа")]
    for case_id, a, b, op, expected in data:
        driver.find_element(By.ID, "clear").click()
        driver.find_element(By.ID, "first").send_keys(a)
        driver.find_element(By.ID, "second").send_keys(b)
        Select(driver.find_element(By.ID, "operation")).select_by_value(op)
        driver.find_element(By.ID, "calculate").click()
        output = driver.find_element(By.ID, "output").text
        actual = output.removeprefix("Результат\n")
        path = screenshot(driver, "lab01", case_id.lower())
        cases.append({"id":case_id,"input":[a,b,op],"expected":expected,"actual":actual,"status":"PASS" if expected == actual else "FAIL","screenshot":path})
    driver.find_element(By.ID, "clear").click()
    empty = all(driver.find_element(By.ID, field).get_attribute("value") == "" for field in ("first","second"))
    actual = "Поля пустые, операция add, результат сброшен" if empty and driver.find_element(By.ID,"operation").get_attribute("value") == "add" and "появится" in driver.find_element(By.ID,"output").text else "Сброс неполный"
    cases.append({"id":"TC10","expected":"Поля пустые, операция add, результат сброшен","actual":actual,"status":"PASS" if actual.startswith("Поля пустые") else "FAIL","screenshot":screenshot(driver,"lab01","tc10_clear")})
    write_results("lab01",driver,cases)
    assert all(case["status"] == "PASS" for case in cases)


def todo_cases(driver,url):
    driver.get(url + "/lab02/app/")
    driver.find_element(By.ID,"reset").click()
    cases=[]
    def add(title):
        driver.find_element(By.ID,"new-task").send_keys(title)
        driver.find_element(By.ID,"add-task").click()
    def titles():
        return [element.text for element in driver.find_elements(By.CSS_SELECTOR,".title")]
    def record(id,expected,actual,name):
        cases.append({"id":id,"expected":expected,"actual":actual,"status":"PASS" if expected == actual else "FAIL","screenshot":screenshot(driver,"lab02",name)})
    add("Подготовить тест-кейсы")
    record("UI01", "['Подготовить тест-кейсы']",str(titles()),"01_add_task")
    add("   ")
    record("UI02", "1 задача",f"{len(titles())} задачи","02_blank_task_bug")
    driver.find_element(By.ID,"reset").click()
    add("Подготовить тест-кейсы");add("Проверить приложение")
    driver.find_elements(By.CSS_SELECTOR,'.todo-row input')[0].click()
    record("UI03", "Осталось активных: 1",driver.find_element(By.ID,'counter').text,"03_counter_bug")
    driver.find_element(By.CSS_SELECTOR,'[data-filter="done"]').click()
    record("UI04", "['Подготовить тест-кейсы']",str(titles()),"04_completed_filter_bug")
    driver.find_element(By.CSS_SELECTOR,'[data-filter="active"]').click()
    record("UI05", "['Проверить приложение']",str(titles()),"05_active_filter")
    driver.find_element(By.CSS_SELECTOR,'[data-filter="all"]').click()
    driver.refresh()
    record("UI06", "['Подготовить тест-кейсы', 'Проверить приложение']",str(titles()),"06_persistence")
    driver.find_elements(By.CSS_SELECTOR,'.todo-row button')[1].click()
    record("UI07", "['Подготовить тест-кейсы']",str(titles()),"07_delete_wrong_task_bug")
    write_results("lab02",driver,cases)
    assert sum(c['status']=='FAIL' for c in cases)==4


if __name__ == "__main__":
    driver = create_browser()
    try:
        calculator_cases(driver,"http://127.0.0.1:8765")
        todo_cases(driver,"http://127.0.0.1:8765")
    finally:
        driver.quit()
