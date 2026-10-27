# ЛР 5. REST API пользователей

API: https://jsonplaceholder.typicode.com. Проверено реальными GET/POST/PUT-запросами. Сервис имитирует создание и обновление: последующий GET не обязан возвращать изменённые данные.

Коллекция: users.postman_collection.json (формат Postman v2.1); переменная base_url встроена, авторизация не нужна. Импорт: Postman → Import → выбрать файл → Run collection. Три запроса содержат 12 JavaScript-проверок: HTTP-код, Content-Type, структура и значения.

Командный запуск той же коллекции:

```powershell
.tools\postman\postman-cli.exe collection run lab05\users.postman_collection.json -r cli,json,html --reporter-json-export lab05\results\postman-run.json --reporter-html-export lab05\results\postman-run.html
```

Python-проверки повторяют GET/POST/PUT и добавляют 404 для отсутствующего пользователя. Команда: `python scripts/run_tests.py lab05`. Фактические запросы и ответы сохраняются отдельно в results/*.json; ключей доступа в них нет.

Источники: [JSONPlaceholder](https://jsonplaceholder.typicode.com/), [Postman CLI collection run](https://learning.postman.com/docs/postman-cli/postman-cli-run-collection), [проверки ответов](https://learning.postman.com/docs/tests-and-scripts/write-scripts/test-scripts).
