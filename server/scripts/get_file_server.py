import socket
from Crypto.Cipher import AES
from datetime import datetime

now = datetime.now()
KEY = b'Sixteen byte key'  # 16-байтный ключ (должен совпадать с сервером)
IV = b'This is an IV456'  # 16-байтный IV (должен совпадать с сервером)

def decrypt_file(encrypted_data):
    try:
        """ Расшифровка полученных данных """
        cipher = AES.new(KEY, AES.MODE_CFB, IV)
        decrypted_data = cipher.decrypt(encrypted_data)
        return decrypted_data
    except Exception as e:
        print(f"Ошибка: {e}")

def receive_file(server_socket, save_path):
    """ Получение и расшифровка файла """
    try:
        encrypted_data = server_socket.recv(4096)  # Получаем данные
        decrypted_data = decrypt_file(encrypted_data)

        with open(save_path, 'wb') as file:
            file.write(decrypted_data)

        print(f"🔓 Файл успешно получен и расшифрован -> {save_path}")
    except Exception as e:
        print(f"Ошибка при получении файла: {e}")
    finally:
        server_socket.close()

def start_client(host):
    try:
        # host = '192.168.2.101'  # IP сервера
        print(host)
        port = 12346  

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        receive_file(client_socket, now.strftime("%Y-%m-%d_%H-%M-%S")+'.txt')
    except Exception as e:
        print(f"Ошибка: {e}")