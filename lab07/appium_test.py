"""Launch own Android app, tap Add, add a note, capture real device screens."""
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "lab07"
PACKAGE = "org.study.notes"
ADB = ROOT / ".tools/android-sdk/platform-tools/adb.exe"


def adb(*args):
    result = subprocess.run([str(ADB),"-s","emulator-5554",*args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    result.check_returncode()
    return result.stdout.strip()


if __name__ == "__main__":
    results = LAB / "results"; results.mkdir(exist_ok=True)
    screens = LAB / "screenshots"; screens.mkdir(exist_ok=True)
    options = UiAutomator2Options().load_capabilities({
        "platformName":"Android", "appium:automationName":"UiAutomator2",
        "appium:deviceName":"TrainingPhone", "appium:udid":"emulator-5554",
        "appium:app":str(LAB/"artifacts/study-notes.apk"), "appium:appPackage":PACKAGE,
        "appium:appActivity":".MainActivity", "appium:noReset":False,
        "appium:newCommandTimeout":180, "appium:adbExecTimeout":120000,
        "appium:uiautomator2ServerInstallTimeout":120000,
        "appium:uiautomator2ServerLaunchTimeout":120000
    })
    checks = []
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    wait = WebDriverWait(driver,30)
    def find(id): return driver.find_element(AppiumBy.ACCESSIBILITY_ID,id)
    def shot(name):
        driver.save_screenshot(str(screens/(name+".png")))
        return f"screenshots/{name}.png"
    def record(id,expected,actual,name):
        row={"id":id,"expected":expected,"actual":actual,"status":"PASS" if actual==expected else "FAIL","screenshot":shot(name)}
        checks.append(row);print(row,flush=True)
    def has_note(): return "Первая заметка" in driver.page_source
    try:
        wait.until(lambda _: find("add_note").is_displayed())
        shot("01_launch")
        find("add_note").click()
        record("M01","Введите текст заметки",find("note_error").text,"02_empty_validation")
        find("note_input").send_keys("Первая заметка")
        find("add_note").click()
        wait.until(lambda _:find("note_count").text=="Заметок: 1")
        record("M02",True,has_note(),"03_note_added")
        driver.orientation="LANDSCAPE"
        wait.until(lambda _:driver.orientation=="LANDSCAPE")
        record("M03",True,has_note(),"04_landscape")
        driver.orientation="PORTRAIT"
        driver.press_keycode(3);driver.activate_app(PACKAGE)
        record("M04",True,has_note(),"05_background_return")
        sms_result = adb("emu","sms","send","5551234","Training message")
        record("M05",True,"OK" in sms_result and has_note(),"06_sms_interruption")
        call_result=adb("emu","gsm","call","5551234")
        time.sleep(2)
        shot("07_incoming_call")
        registry=adb("shell","dumpsys","telephony.registry")
        (results/"telephony.txt").write_text(registry,encoding="utf-8")
        adb("emu","gsm","cancel","5551234")
        driver.activate_app(PACKAGE)
        record("M06",True,"OK" in call_result and has_note(),"08_after_call")
        adb("shell","am","force-stop",PACKAGE);driver.activate_app(PACKAGE)
        wait.until(lambda _:find("add_note").is_displayed())
        record("M07",True,has_note(),"09_process_restart")
        before=adb("shell","dumpsys","meminfo",PACKAGE)
        for index in range(15):
            find("note_input").send_keys(f"Заметка {index+2}");find("add_note").click()
        driver.execute_script("mobile: scrollGesture",{"left":50,"top":600,"width":900,"height":1000,"direction":"down","percent":.8})
        after=adb("shell","dumpsys","meminfo",PACKAGE)
        (results/"memory-before.txt").write_text(before,encoding="utf-8")
        (results/"memory-after.txt").write_text(after,encoding="utf-8")
        record("M08","Заметок: 16",find("note_count").text,"10_scroll_and_memory")
        find("note_input").send_keys("Черновик")
        driver.orientation="LANDSCAPE"
        wait.until(lambda _:find("note_input").text=="Черновик")
        record("M09","Черновик",find("note_input").text,"11_draft_after_rotation")
        driver.orientation="PORTRAIT"
        driver.hide_keyboard()
        shot("12_final_notes")
    finally:
        info={"executed_at":datetime.now().astimezone().isoformat(),"device":adb("shell","getprop","ro.product.model"),"android":adb("shell","getprop","ro.build.version.release"),"method":"Actual emulator/Appium interaction; human manual execution is not claimed","checks":checks}
        (results/"mobile-checks.json").write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding="utf-8")
        driver.quit()
    assert len(checks)==9 and all(c['status']=='PASS' for c in checks)
