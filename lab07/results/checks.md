# Результаты проверки Android

Дата: 2026-10-28T02:27:04.041548+03:00
Устройство: sdk_gphone_x86_64; Android 11

| Сценарий | Результат | Скриншот |
|---|---|---|
| M01 | PASS | [02_empty_validation.png](../screenshots/02_empty_validation.png) |
| M02 | PASS | [03_note_added.png](../screenshots/03_note_added.png) |
| M03 | PASS | [04_landscape.png](../screenshots/04_landscape.png) |
| M04 | PASS | [05_background_return.png](../screenshots/05_background_return.png) |
| M05 | PASS | [06_sms_interruption.png](../screenshots/06_sms_interruption.png) |
| M06 | PASS | [08_after_call.png](../screenshots/08_after_call.png) |
| M07 | PASS | [09_process_restart.png](../screenshots/09_process_restart.png) |
| M08 | PASS | [10_scroll_and_memory.png](../screenshots/10_scroll_and_memory.png) |
| M09 | PASS | [11_draft_after_rotation.png](../screenshots/11_draft_after_rotation.png) |

PSS до добавления 15 заметок: 22231 КБ. После: 27583 КБ. Значения взяты из dumpsys meminfo; исходный вывод сохранен рядом.

Все 9 сценариев прошли. Входящий звонок подтвержден состоянием mCallState=1 в telephony.txt. После прерываний и перезапуска процесса заметка сохранилась. При повороте проверялось не только значение ориентации, но и фактическая ширина кнопки после перестроения интерфейса.

M08 подтверждает короткую проверку добавления и прокрутки без падения. Длительное наблюдение за утечками памяти не выполнялось.
