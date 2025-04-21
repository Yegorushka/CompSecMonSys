import requests
import json

TOKEN = ''


def send_file_to_telegram(FILE_PATH, chat_id):
    """Функция для отправки файла в Telegram."""
    if not chat_id:
        # print("\n⚠️ Операция отменена: chat_id не найден.")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(FILE_PATH, "rb") as file:
        files = {"document": file}
        data = {"chat_id": chat_id}
        response = requests.post(url, data=data, files=files)

        try:
            response_data = response.json()  # Преобразуем в JSON
        except json.JSONDecodeError:
            return
