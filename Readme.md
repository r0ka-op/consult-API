
# API  для пд


## Установка и запуск

1. Клонируйте:
   ```
   git clone https://github.com/r0ka-op/consult-API.git
   cd consult-API
   ```

2. Создайте и активируйте виртуальное окружение:
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Запустите сервер:
   ```
   python app.py    # Необходимо чтобы таблица успешно создалась
   gunicorn -w 3 -b localhost:5050 --log-file=gunicorn.log --pid=/var/run/gunicorn-consult-API-flask.pid app:app
   ```

Сервер будет доступен по адресу `http://localhost:5050`.

## Эндпоинты API

### Отправить заявку

- **URL:** `/add_consult`
- **Метод:** POST
- **Тело запроса:**
  ```json
  {
    "student_name": "Иван",
    "group": "241-3210",
    "mentor": "Дмитрий",
    "topic": "Виды подключения к Интернету.",
    "comments": "",
    "discord": "@abcdefg"
  }
  ```
- **Успешный ответ:** Код 201
  ```json
  {
    "id": 1,
    "student_name": "Иван",
    "group": "241-3210",
    "mentor": "Дмитрий",
    "topic": "Виды подключения к Интернету.",
    "comments": "",
    "discord": "@abcdefg",
    "is_accepted" False
  }
  ```

### Получить заявку

- **URL:** `/consults/<consult_id>`
- **Метод:** GET
- **Успешный ответ:** Код 200
  ```json
  {
    "id": 1,
    "student_name": "Иван",
    "group": "241-3210",
    "mentor": "Дмитрий",
    "topic": "Виды подключения к Интернету.",
    "comments": "",
    "discord": "@abcdefg",
    "is_accepted" False
  }
  ```

### Получить список заявок

- **URL:** `/consults`
- **Метод:** GET
- **Успешный ответ:** Код 200
  ```json
  [
    {
    "id": 1,
    "student_name": "Иван",
    "group": "241-3210",
    ...
    },
    {
    "id": 2,
    "student_name": "Мария",
    "group": "241-321",
    ...
    }
  ]
  ```

### Изменить заявку

- **URL:** `/consults/<consult_id>`
- **Метод:** PUT
- **Тело запроса (все поля опциональны):**
  ```json
  {
    "student_name": "Иван Иванов",
    "group": "241-321",
    "mentor": "Елена",
    "topic": "Сетевые протоколы",
    "comments": "Прошу перенести консультацию",
    "discord": "@ivanov",
    "is_accepted" False
  }
  ```
- **Успешный ответ:** Код 200
  ```json
  {
    "id": 1,
    "student_name": "Иван Иванов",
    "group": "241-321",
    "mentor": "Елена",
    "topic": "Сетевые протоколы",
    "comments": "Прошу перенести консультацию",
    "discord": "@ivanov",
    "is_accepted" False
  }
  ```

### Изменить статус заявку

- **URL:** `consults/toggle-status/<int:consult_id>`
- **Метод:** POST
- **Успешный ответ:** Код 200
  ```json
  {
    "id": 1,
    "student_name": "Иван Иванов",
    "group": "241-321",
    "mentor": "Елена",
    "topic": "Сетевые протоколы",
    "comments": "Прошу перенести консультацию",
    "discord": "@ivanov",
    "is_accepted" True
  }
  ```

### Удалить заявку

- **URL:** `/consults/<consult_id>`
- **Метод:** DELETE
- **Успешный ответ:** Код 200
  ```json
  {
    "message": "Заявка с id 1 удалена из базы данных"
  }
  ```

## Тестирование

Для тестирования API используйте скрипт `test_api.py`. Запустите его командой:

```
python test_api.py
```

Этот скрипт выполнит серию тестов для проверки всех эндпоинтов API.

***


## Таблица с эндпоинтами и примерами (часть старого оформления)


| **ФТ**                 | **Endpoint**           | **HTTP-метод** | **Параметры запроса**             | **Пример тела запроса**                                                                                                                                                                                                                             | **Пример тела ответа**                                                                                                                                                                                                                                                                                        |
| ---------------------- | ---------------------- | -------------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Отправить заявку       | /add_consult           | POST           | Без параметров                    | {<br> "student_name": "Иван",<br> "group": "241-3210",<br> "mentor": "Дмитрий",<br> "preferred_date": "2024-09-30",<br> "preferred_time": "16:00",<br> "topic": "Виды подключения к Интернету.",<br> "comments": "",<br> "discord": "@abcdefg111111111111111111111111111111111111"<br>} | {<br> "id": 1,<br> "student_name": "Иван",<br> "group": "241-3210",<br> "mentor": "Дмитрий",<br> "preferred_date": "2024-09-30",<br> "preferred_time": "16:00:00",<br> "topic": "Виды подключения к Интернету.",<br> "comments": "",<br> "discord": "@abcdefg111111111111111111111111111111111111"<br>}                                           |
| Получить заявку        | /consults/<consult_id> | GET            | consult_id - ID заявки в пути URL | Нет тела запроса                                                                                                                                                                                                                                    | {<br> "id": 1,<br> "student_name": "Иван",<br> "group": "241-3210",<br> "mentor": "Дмитрий",<br> "preferred_date": "2024-09-30",<br> "preferred_time": "16:00:00",<br> "topic": "Виды подключения к Интернету.",<br> "comments": "",<br> "discord": "@abcdefg111111111111111111111111111111111111"<br>}                                           |
| Получить список заявок | /consults              | GET            | Без параметров                    | Нет тела запроса                                                                                                                                                                                                                                    | [<br> {<br> "id": 1,<br> "student_name": "Иван",<br> "group": "241-3210",<br> ...<br> },<br> {<br> "id": 2,<br> "student_name": "Мария",<br> "group": "241-321",<br> ...<br> }<br>]                                                                                                                          |
| Изменить заявку        | /consults/<consult_id> | PUT            | consult_id - ID заявки в пути URL | {<br> "student_name": "Иван Иванов",<br> "preferred_time": "17:00",<br> "comments": "Прошу перенести время консультации."<br>}                                                                                                                      | {<br> "id": 1,<br> "student_name": "Иван Иванов",<br> "group": "241-3210",<br> "mentor": "Дмитрий",<br> "preferred_date": "2024-09-30",<br> "preferred_time": "17:00:00",<br> "topic": "Виды подключения к Интернету.",<br> "comments": "Прошу перенести время консультации.",<br> "discord": "@abcdefg"<br>} |
| Удалить заявку         | /consults/<consult_id> | DELETE         | consult_id - ID заявки в пути URL | Нет тела запроса                                                                                                                                                                                                                                    | {<br> "message": "Заявка с id 1 удалена из базы данных"<br>}                                                                                                                                                                                                                                                  |


