import requests
import json

BASE_URL = "http://localhost:5000"


def test_add_consult():
    url = f"{BASE_URL}/add_consult"
    data = {
        "student_name": "Иван",
        "group": "241-3210",
        "mentor": "Дмитрий",
        "preferred_date": "2024-09-30",
        "preferred_time": "16:00",
        "topic": "Виды подключения к Интернету.",
        "comments": "",
        "discord": "@ivanov"
    }
    response = requests.post(url, json=data)
    print("Добавление заявки:")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.json().get('id')


def test_get_consult(consult_id):
    url = f"{BASE_URL}/consults/{consult_id}"
    response = requests.get(url)
    print(f"\nПолучение заявки (id={consult_id}):")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_get_all_consults():
    url = f"{BASE_URL}/consults"
    response = requests.get(url)
    print("\nПолучение всех заявок:")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_update_consult(consult_id):
    url = f"{BASE_URL}/consults/{consult_id}"
    data = {
        "student_name": "Иван Иванов",
        "group": "241-3211",
        "mentor": "Елена",
        "preferred_date": "2024-10-01",
        "preferred_time": "17:00",
        "topic": "Сетевые протоколы",
        "comments": "Прошу перенести консультацию",
        "discord": "@ivanov_updated"
    }
    response = requests.put(url, json=data)
    print(f"\nОбновление заявки (id={consult_id}):")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_partial_update_consult(consult_id):
    url = f"{BASE_URL}/consults/{consult_id}"
    data = {
        "preferred_time": "18:00",
        "comments": "Изменено только время и комментарий"
    }
    response = requests.put(url, json=data)
    print(f"\nЧастичное обновление заявки (id={consult_id}):")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_delete_consult(consult_id):
    url = f"{BASE_URL}/consults/{consult_id}"
    response = requests.delete(url)
    print(f"\nУдаление заявки (id={consult_id}):")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


if __name__ == "__main__":
    # Запуск тестов
    consult_id = test_add_consult()
    if consult_id:
        test_get_consult(consult_id)
        test_get_all_consults()
        test_update_consult(consult_id)
        test_partial_update_consult(consult_id)
        test_get_consult(consult_id)  # Проверяем результат обновления
        test_delete_consult(consult_id)
    else:
        print("Не удалось добавить заявку. Остальные тесты пропущены.")
