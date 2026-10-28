# ТПО

Лабораторные работы по тестированию программного обеспечения.

1. [Калькулятор и тестовая документация](lab01).
2. [Поиск ошибок в списке задач](lab02).
3. [Проверка входа через Selenium](lab03).
4. [Проверка формы, Page Object](lab04).
5. [REST API, Postman и Python](lab05).
6. [Модульные тесты калькулятора](lab06).
7. [Android-приложение и Appium](lab07).
8. [Нагрузочные тесты k6](lab08).
9. [GitHub Actions](lab09).

## Запуск

Нужны Python и Chrome. Команды выполняются из папки проекта:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.venv\Scripts\python.exe server.py
```

Приложения откроются по адресу http://127.0.0.1:8765.

Запуск автотестов в другом терминале:

```powershell
.venv\Scripts\python.exe scripts\run_tests.py lab03 lab04 lab05 lab06
```

Для Android, Postman и k6 команды указаны в папках соответствующих работ.

[Короткие команды запуска ЛР 5-9](ЗАПУСК.md).

Скриншоты находятся в `labXX/screenshots`, результаты запусков в `labXX/results`. Полный список изображений находится в [SCREENSHOTS.md](SCREENSHOTS.md).

Вторая работа содержит намеренные ошибки. Остальные приложения и тесты рассчитаны на успешный прогон.

Учебные отчеты пока не оформлены.
