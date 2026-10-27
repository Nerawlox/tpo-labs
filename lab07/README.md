# ЛР 7. Мобильное приложение «Заметки»

Собственное нативное приложение Android на Java. Поддерживает добавление и удаление заметок, запрет пустого ввода, сохранение списка на устройстве, сохранение черновика и восстановление после поворота/возврата из фона.

APK: artifacts/study-notes.apk. Исходник: src/org/study/notes/MainActivity.java. Манифест: AndroidManifest.xml. Приложение использует только Android SDK, внешних библиотек и Gradle не требует. Отладочная подпись предназначена для учебного запуска.

## Окружение и запуск

Локально подготовлены JDK 21, Android SDK Platform 35, Build Tools 35.0.0, эмулятор Android 11 / API 30 Google APIs x86_64. WHPX подтверждён как доступный; AVD TrainingPhone хранится внутри .tools/avd. Appium 3.9.0, UiAutomator2 8.7.2 и Python-клиент зафиксированы в материалах окружения.

```powershell
.venv\Scripts\python.exe lab07\build.py
.venv\Scripts\python.exe lab07\prepare_emulator.py
.\lab07\start_emulator.ps1
```

Дождаться устройства: `.tools\android-sdk\platform-tools\adb.exe -s emulator-5554 shell getprop sys.boot_completed` должно вывести 1. Эмулятор запускается без отдельного окна; изображения снимаются с его экрана.

В другом терминале запустить `.\lab07\start_appium.ps1`, затем `.venv\Scripts\python.exe lab07\appium_test.py`. Скрипт создаёт новую тестовую сессию приложения и сохраняет фактические результаты и скриншоты.

При подготовке на другом компьютере: `python scripts/provision_tools.py`; `npm install --prefix .tools/appium appium@3.9.0`; установить APPIUM_HOME в .tools/appium-home и выполнить `.tools\appium\node_modules\.bin\appium.cmd driver install uiautomator2@8.7.2`.

## Чек-лист мобильных проверок

| ID | Действие | Ожидаемое поведение |
|---|---|---|
| M01 | Тап «Добавить заметку» с пустым полем | «Введите текст заметки», список не меняется |
| M02 | Ввести текст, тап «Добавить заметку» | Заметка видна, счётчик 1 |
| M03 | Повернуть экран в landscape | Заметка сохраняется, интерфейс доступен |
| M04 | Уйти на домашний экран и вернуться | Список остаётся прежним |
| M05 | Вызвать входящее SMS средствами эмулятора | После прерывания данные не потеряны |
| M06 | Вызвать входящий звонок и отменить | После звонка данные не потеряны |
| M07 | Завершить процесс и запустить снова | Сохранённая заметка восстановлена |
| M08 | Добавить 15 заметок, прокрутить список, снять meminfo до/после | 16 заметок, список прокручивается, приложение не падает |
| M09 | Ввести черновик и повернуть экран | Черновик не теряется |

Appium выполнил все 9 сценариев успешно. Фактические результаты: results/checks.md и results/mobile-checks.json. Измерения памяти сохранены в memory-before.txt и memory-after.txt. Это короткая проверка работы с памятью, не доказательство отсутствия утечек. Прерывания имитировались средствами Android Emulator, физический телефон и реальная сотовая сеть не использовались.

Документация: [Appium](https://appium.io/docs/en/latest/quickstart/install/), [ускорение Android Emulator](https://developer.android.com/studio/run/emulator-acceleration), [Android CLI](https://developer.android.com/tools/agents/android-cli).
