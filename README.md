# Лабораторные работы по тестированию ПО

Девять учебных работ: приложения, тестовая документация, автотесты и фактические результаты проверок. Оформленные учебные отчёты в этот проект не входят.

## Быстрый запуск на Windows

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.venv\Scripts\python.exe server.py
```

Открыть http://127.0.0.1:8765. Установленный Chrome используется Selenium через автоматический подбор драйвера. Для первого запуска драйвера нужен доступ в интернет.

В другом терминале из корня проекта:

```powershell
.venv\Scripts\python.exe scripts\browser_checks.py
.venv\Scripts\python.exe scripts\run_tests.py lab03 lab04 lab05 lab06
.venv\Scripts\python.exe scripts\capture_runs.py
```

browser_checks.py воспроизводит 10 сценариев калькулятора и 7 сценариев списка задач. У списка задач четыре требования намеренно нарушены: протокол фиксирует FAIL и соответствующие дефекты. Это учебная версия для исследования ошибок.

## Содержание

| Работа | Исходники и материалы | Результаты |
|---|---|---|
| 1. Тест-дизайн | lab01/app, test-design.md | 10 UI-сценариев, снимки состояний |
| 2. Дефекты UI | lab02/app, testing-notes.md, bugs.xlsx | 7 сценариев, 4 воспроизводимых дефекта |
| 3. Selenium | lab03/app, test_login.py, smoke_browser.py, selectors.md | 2 автотеста, скриншоты входа/выхода |
| 4. Page Object | lab04/app, pages, test_contact.py, decision-matrix.md | 12 сценариев формы, включая матрицу 2³ |
| 5. REST API | lab05/users.postman_collection.json, test_users_api.py | 12 проверок Postman и 4 pytest-теста |
| 6. Unit-тесты | lab06/calculator.py, test_calculator.py | 50 параметризованных случаев |
| 7. Android/Appium | lab07/src, AndroidManifest.xml, build.py, appium_test.py | Настройка эмулятора и прогон выполняются |
| 8. k6 | lab08/load.js, run_load.py, ../server.py | Два профиля: 10 VUs × 30 с и 50 VUs × 10 с |
| 9. GitHub Actions | .github/workflows/run-tests.yml, lab09 | Публикация и проверка CI выполняются |

В каждой работе папка screenshots содержит PNG-снимки реального браузера или эмулятора. Папка results содержит исходные протоколы и вывод инструментов. HTML-файлы test-run.html и postman-run.html — технические результаты инструментов, не оформленные учебные отчёты.

## Особенности окружения

Основной локальный прогон: Windows, Python 3.14, Chrome. CI: Ubuntu и Python 3.12. Точные версии Python-зависимостей зафиксированы в requirements-lock.txt.

Дополнительные инструменты устанавливаются под .tools: JDK 21, Android SDK, Appium, k6 и Postman CLI. .tools, .venv, временные файлы и исходные документы с титульным листом исключены из Git. Учётные данные стенда №3 — общедоступная учебная пара student / Study123!, не пароль внешнего аккаунта.

Лабораторные №1–4 и №7 содержат пошаговые UI-проверки. Там, где действия воспроизведены скриптом Selenium/Appium, метод явно указан в протоколе. Ручной прогон человеком не заявляется.
