import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QLabel
from PyQt5.QtCore import pyqtSignal, QObject
from datetime import datetime
from Crypto.Cipher import AES

now = datetime.now()
SAVE_PATH = now.strftime("%Y-%m-%d_%H-%M-%S")+'.txt'

UDP_PORT = 37021
TCP_PORT = 5002
BUFFER_SIZE = 4096
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


# Класс-сигнал для общения между потоками и GUI
class SignalHandler(QObject):
    file_received = pyqtSignal()


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Сервер приема файла")
        self.resize(300, 90)

        # Интерфейс
        self.checkbox = QCheckBox("Принимать файл")
        self.status_label = QLabel("Ожидание...")

        layout = QVBoxLayout()
        layout.addWidget(self.checkbox)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        # Сигналы
        self.signals = SignalHandler()
        self.signals.file_received.connect(self.on_file_received)

        self.checkbox.stateChanged.connect(self.toggle_server)

    def toggle_server(self, state):
        if self.checkbox.isChecked():
            print("[✓] Сервер активирован.")
            threading.Thread(target=self.udp_listener, daemon=True).start()
            threading.Thread(target=self.tcp_file_receiver, daemon=True).start()
            self.status_label.setText("Ожидание подключения клиента...")
        else:
            print("[i] Сервер не активен.")
            self.status_label.setText("Остановлено.")

    def udp_listener(self):
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.bind(('', UDP_PORT))
        print(f"[UDP] Ожидание broadcast на {UDP_PORT}...")
        while self.checkbox.isChecked():
            try:
                data, addr = udp_sock.recvfrom(1024)
                if data.decode() == "DISCOVER_SERVER":
                    server_ip = socket.gethostbyname(socket.gethostname())
                    print(f"[UDP] Ответ клиенту {addr}, IP: {server_ip}")
                    udp_sock.sendto(server_ip.encode(), addr)
            except Exception as e:
                print(f"[UDP] Ошибка: {e}")
                break
        udp_sock.close()

    def tcp_file_receiver(self):
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.bind(('', TCP_PORT))
        tcp_sock.listen(1)
        print(f"[TCP] Ожидание файла на порту {TCP_PORT}...")

        try:
            conn, addr = tcp_sock.accept()
            print(f"[TCP] Подключено: {addr}")
            with open(SAVE_PATH, "wb") as f:
                while True:
                    encrypted_data = conn.recv(BUFFER_SIZE)
                    data = decrypt_file(encrypted_data)
                    if not data:
                        break
                    f.write(data)
            print(f"[✓] Файл получен и сохранен как {SAVE_PATH}")
            self.signals.file_received.emit()
            conn.close()
        except Exception as e:
            print(f"[TCP] Ошибка: {e}")
        finally:
            tcp_sock.close()

    def on_file_received(self):
        self.checkbox.setChecked(False)
        self.status_label.setText(f"✅ Файл {SAVE_PATH} получен и разшифрован.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
