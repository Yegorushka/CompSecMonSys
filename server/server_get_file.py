import socket
import threading
import sys
import ssl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QLabel
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from datetime import datetime

now = datetime.now()
SAVE_PATH = now.strftime("%Y-%m-%d_%H-%M-%S")+'.txt'

UDP_PORT = 37021
TCP_PORT = 5002
BUFFER_SIZE = 4096

# Сертификаты для SSL
CERT_FILE = 'ssl\\server.crt'
KEY_FILE = 'ssl\\server.key'


# Класс-сигнал для общения между потоками и GUI
class SignalHandler(QObject):
    file_received = pyqtSignal()


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Сервер приема файла")
        self.resize(300, 90)
        self.setWindowIcon(QIcon("img\\download.png"))

        # Интерфейс
        self.checkbox = QCheckBox("Принимать файл")
        self.attention_label = QLabel("❗️Оптимально Вы можете запустить сервер один раз.\nПри повторном запуске возможна ошибка.\nПерезапустите программу❗️")
        self.status_label = QLabel("Ожидание...")

        layout = QVBoxLayout()
        layout.addWidget(self.checkbox)
        layout.addWidget(self.attention_label)
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

        # Оборачиваем сокет в SSL
        ssl_sock = ssl.wrap_socket(tcp_sock, keyfile=KEY_FILE, certfile=CERT_FILE, server_side=True)

        try:
            conn, addr = ssl_sock.accept()
            print(f"[TCP][SSL] Подключено: {addr}")
            with open(SAVE_PATH, "wb") as f:
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        break
                    f.write(data)
        except Exception as e:
            print(f"[TCP] Ошибка: {e}")
        finally:
            print(f"[✓] Файл получен и сохранен как {SAVE_PATH}")
            self.signals.file_received.emit()
            ssl_sock.close()
            tcp_sock.close()
            conn.close()

    def on_file_received(self):
        self.checkbox.setChecked(False)
        self.status_label.setText(f"✅ Файл {SAVE_PATH} получен.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
