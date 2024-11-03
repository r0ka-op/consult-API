
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
    "mentor": "Дмитрий", 
    "topic": "Виды подключения к Интернету",
    "comments": "",
    "specialization": "net"
  }
  ```
- **Успешный ответ:** Код 201
  ```json
  {
    "id": 1,
    "student_name": "Иван",
    "mentor": "Дмитрий",
    "topic": "Виды подключения к Интернету",
    "comments": "",
    "specialization": "net",
    "is_accepted": false
  }
  ```
- **Ошибки:**
  - 400: Отсутствует обязательное поле или некорректное значение specialization
  - 500: Ошибка базы данных

### Получить заявку

- **URL:** `/consults/<consult_id>`
- **Метод:** GET
- **Успешный ответ:** Код 200
  ```json
  {
    "id": 1,
    "student_name": "Иван",
    "mentor": "Дмитрий",
    "topic": "Виды подключения к Интернету",
    "comments": "",
    "specialization": "net",
    "is_accepted": false
  }
  ```
- **Ошибки:**
  - 404: Заявка не найдена

### Получить список заявок

- **URL:** `/consults`
- **Метод:** GET
- **Успешный ответ:** Код 200
  ```json
  [
    {
      "id": 1,
      "student_name": "Иван",
      "mentor": "Дмитрий",
      "topic": "Виды подключения к Интернету",
      "comments": "",
      "specialization": "net",
      "is_accepted": false
    },
    {
      "id": 2,
      "student_name": "Мария",
      "mentor": "Елена", 
      "topic": "JavaScript Basics",
      "comments": "",
      "specialization": "web",
      "is_accepted": false
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
    "mentor": "Елена",
    "topic": "Сетевые протоколы",
    "comments": "Прошу перенести консультацию",
    "specialization": "net",
    "is_accepted": false
  }
  ```
- **Успешный ответ:** Код 200
  ```json
  {
    "id": 1,
    "student_name": "Иван Иванов",
    "mentor": "Елена",
    "topic": "Сетевые протоколы", 
    "comments": "Прошу перенести консультацию",
    "specialization": "net",
    "is_accepted": false
  }
  ```
- **Ошибки:**
  - 400: Некорректное значение specialization
  - 404: Заявка не найдена
  - 500: Ошибка базы данных

### Изменить статус заявки

- **URL:** `/consults/toggle-status/<consult_id>`
- **Метод:** PATCH
- **Успешный ответ:** Код 200
  ```json
  {
    "id": 1,
    "student_name": "Иван Иванов",
    "mentor": "Елена",
    "topic": "Сетевые протоколы",
    "comments": "Прошу перенести консультацию", 
    "specialization": "net",
    "is_accepted": true
  }
  ```
- **Ошибки:**
  - 404: Заявка не найдена
  - 500: Ошибка базы данных

### Принять заявку

- **URL:** `/consults/<consult_id>/accept`
- **Метод:** PATCH
- **Успешный ответ:** Код 200
  ```json
  {
    "id": 1,
    "student_name": "Иван Иванов",
    "mentor": "Елена",
    "topic": "Сетевые протоколы",
    "comments": "Прошу перенести консультацию",
    "specialization": "net", 
    "is_accepted": true
  }
  ```
- **Ошибки:**
  - 404: Заявка не найдена
  - 500: Ошибка базы данных

### Удалить заявку

- **URL:** `/consults/<consult_id>`
- **Метод:** DELETE 
- **Успешный ответ:** Код 200
  ```json
  {
    "message": "Заявка с id 1 удалена из базы данных"
  }
  ```
- **Ошибки:**
  - 404: Заявка не найдена






## Тестирование

Для тестирования API используйте скрипт `test_api.py`. Запустите его командой:

```
python test_api.py
```

Этот скрипт выполнит серию тестов для проверки всех эндпоинтов API.

***

