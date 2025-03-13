import requests
import json

TOKEN = 'XXXXX'
CHAT_ID_FILE = "scripts\\telegram\\chat_id.txt"  # Файл с chat_id

def get_chat_id():
    """Функция для чтения chat_id из файла."""
    try:
        with open(CHAT_ID_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()  # Убираем лишние пробелы и переносы строк
    except FileNotFoundError:
        print("\n❌ Ошибка: Файл 'chat_id.txt' не найден!")
        return None
    except Exception as e:
        print(f"\n❌ Ошибка при чтении chat_id: {e}")
        return None

def send_file_to_telegram(FILE_PATH):
    """Функция для отправки файла в Telegram."""
    chat_id = get_chat_id()
    if not chat_id:
        print("\n⚠️ Операция отменена: chat_id не найден.")
        return
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(FILE_PATH, "rb") as file:
        files = {"document": file}
        data = {"chat_id": chat_id}
        response = requests.post(url, data=data, files=files)
        
        try:
            response_data = response.json()  # Преобразуем в JSON
            if response_data.get("ok"):
                print("\n✅ Файл успешно отправлен!")
                print(f"📄 Название файла: {FILE_PATH}")
                print(f"📩 Отправлено в чат: {response_data['result']['chat']['id']}")
                print(f"📎 File ID: {response_data['result']['document']['file_id']}")
                print(f"🕒 Дата отправки: {response_data['result']['date']}")
            else:
                print("\n❌ Ошибка при отправке файла!")
                print(f"⚠ Код ошибки: {response_data['error_code']}")
                print(f"📌 Описание: {response_data['description']}")
        except json.JSONDecodeError:
            print("\n❌ Ошибка! Не удалось обработать ответ от сервера.")
            print(f"Ответ сервера (не JSON): {response.text}")
