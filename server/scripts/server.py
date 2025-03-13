import socket
import time

ip_address = ''

###########################################################
port = 12345
response_message = b"I am the server"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', port))
sock.settimeout(10) # Установим таймаут на 10 секунд

print("Ожидание подключения клиента...")

try:
    while True:
        try:
            data, client_address = sock.recvfrom(1024)
            if data == b"Who is the server?":
                sock.sendto(response_message, client_address)
                break
        except socket.timeout:
            print("Таймаут: Ответ от клиента не получен за 10 секунд.")
            break
except Exception as e:
    print(f"Ошибка: {e}")

###########################################################

# Настройка сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))  # Слушать на всех интерфейсах, порт 12345
server_socket.listen(1)
server_socket.settimeout(5) # Установим таймаут на 10 секунд

# Получение и отправка сообщений
try:
    client_socket, client_address = server_socket.accept()
    print(f"Клиент подключен: {client_address}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            ip_address = message
            # if message.lower() == 'exit':
            #     print("Закрытие соединения...")
            #     break

            print(f"IP-адрес клиента: {message}")
            client_socket.send("Сообщение получено".encode('utf-8'))
            break
        except socket.timeout:
            print("Таймаут: Ответ от клиента не получен за 10 секунд.")
            break
except Exception as e:
    print(f"Ошибка: {e}")

# Закрытие соединения
client_socket.close()
server_socket.close()



# Этот код реализует сервер с двумя частями: 

# 1. **UDP-сервер**:
#    - Открывает порт 12345 для работы с протоколом UDP.
#    - Принимает сообщение от клиента.
#    - Если сообщение содержит строку `"Who is the server?"`, отправляет клиенту ответное сообщение `"I am the server"` и завершает цикл.

# 2. **TCP-сервер**:
#    - Открывает порт 12345 для работы с протоколом TCP, принимая подключения от клиента.
#    - Ожидает подключения клиента и принимает сообщение.
#    - Сохраняет полученное сообщение (предположительно IP-адрес клиента) в переменную `ip_address`.
#    - Отправляет клиенту подтверждение получения сообщения.
#    - Завершает соединение и закрывает сокет.

# Код работает с двумя различными протоколами (UDP и TCP) для демонстрации передачи данных.
