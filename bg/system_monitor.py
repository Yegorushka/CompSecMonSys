import os
import time
import psutil
import platform
import socket
import json

LOG_FILE = "C:\\Users\\(x_x)\\Study\\Диплом\\CompSecMonSys\\bg\\system_monitor.log"  # Файл для логов

def get_system_info():
    """Собирает информацию о системе"""
    return {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Hostname": socket.gethostname(),
        "CPU Usage (%)": psutil.cpu_percent(),
        "RAM Usage (%)": psutil.virtual_memory().percent,
        "Disk Usage (%)": psutil.disk_usage('/').percent,
        "IP Address": socket.gethostbyname(socket.gethostname())
    }

def write_log():
    """Записывает данные в файл"""
    data = get_system_info()
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4) + "\n")

write_log()
# def run_background():
#     """Запуск в фоновом режиме"""
#     while True:
#         write_log()
#         time.sleep(10)  # Интервал обновления данных (60 секунд)

# if __name__ == "__main__":
#     run_background()
