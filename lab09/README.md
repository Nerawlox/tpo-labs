# ЛР 9. Автоматический запуск тестов

Конфигурация: ../.github/workflows/run-tests.yml. События: push в main, pull_request и ручной workflow_dispatch.

Два задания на Ubuntu с Python 3.12:

1. unit-tests - 50 параметризованных случаев Calculator из №6.
2. ui-tests - 14 Selenium-сценариев авторизации и контактной формы из №3-4. Локальный сервер поднимается фикстурой pytest на свободном порту.

Оба задания устанавливают зафиксированные зависимости. При любом исходе сохраняются JUnit-файлы; UI-задание также сохраняет скриншоты. API внешнего сервиса не включён в обязательный CI, чтобы его недоступность не влияла на проверку собственного кода.

Репозиторий: https://github.com/Nerawlox/tpo-labs.

Первый реальный запуск: https://github.com/Nerawlox/tpo-labs/actions/runs/40600682095. Оба задания завершились успешно: 50 unit-тестов и 14 UI-тестов. Статус и сведения о заданиях сохранены в results/actions-run-40600682095.json, снимок страницы в screenshots/01_actions_success.jpg.

Источник: [GitHub - Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).
