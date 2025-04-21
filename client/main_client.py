from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

import sys
import os

try:
    Form, _ = uic.loadUiType("main_client.ui")
except Exception as e:
    print(f"❌Ошибка загрузки UI: {e}")
    sys.exit(1)

destination = os.path.join("C:\\Users", os.getlogin(), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup") 
source_parameters = 'parameters.txt'


class Ui(QtWidgets.QMainWindow, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)

        self.pushButton_send_file.clicked.connect(self.on_button_send_file)

        self.counter = 0
        self.checkBox_auto_search.stateChanged.connect(self.toggle_timer)
        self.comboBox_time.addItems(["3 секунды", "10 секунд", "30 секунд", "60 секунд"])
        self.comboBox_time.currentIndexChanged.connect(self.change_interval)
        self.intervals = {
            "3 секунды": 3000,
            "10 секунд": 10000,
            "30 секунд": 30000,
            "60 секунд": 60000
        }
        self.current_interval = 5000        # Интервал по умолчанию: 1 секунда
        self.timer = QtCore.QTimer(self)    # Создаем таймер
        self.timer.timeout.connect(self.on_button_click_client)

        self.pushButton_create_info.clicked.connect(self.on_button_create_info)

        with open('tele_bot/chat_id.txt', "r", encoding="utf-8") as file:
            text = file.read().strip()
            self.lineEdit_tele_id.setText(text)

        self.pushButton_save_tele_id.clicked.connect(self.save_chat_id)
        self.pushButton_send_tele.clicked.connect(self.send_tele)
        self.pushButton_set_file.clicked.connect(self.set_file)

        self.pushButton_save_auto.clicked.connect(self.on_button_create_info_auto)
        self.checkBox_autostart_auto.stateChanged.connect(self.toggle_text_checkbox)
        self.load_checkbox_state()

    def load_checkbox_state(self):
        """Читает файл и устанавливает состояние чекбокса"""
        path_parameters = os.path.join(destination, source_parameters)
        if os.path.exists(path_parameters):
            with open(path_parameters, "r", encoding="utf-8") as file:
                content = file.read().strip().lower()
                if "autostart on" in content:
                    self.checkBox_autostart_auto.setChecked(True)
                    self.checkBox_autostart_auto.setText("Включенный автозапуск")
                else:
                    self.checkBox_autostart_auto.setChecked(False)
                    self.checkBox_autostart_auto.setText("Выключенный автозапуск")
        else:
            self.checkBox_autostart_auto.setChecked(False)
            self.checkBox_autostart_auto.setText("Выключенный автозапуск")

    def toggle_text_checkbox(self, state):
        """Меняет текст чекбокса при активации/деактивации"""
        if state == 2:  # Qt.Checked
            self.checkBox_autostart_auto.setText("Включенный автозапуск")
        else:
            self.checkBox_autostart_auto.setText("Выключенный автозапуск")

    def on_button_create_info_auto(self):
        import shutil

        QApplication.setOverrideCursor(Qt.WaitCursor)
        report = []

        if self.checkBox_port_auto.isChecked():
            report.append("ports on\n")

        if self.checkBox_sys_info_auto.isChecked():
            report.append("sys_info on\n")

        if self.checkBox_active_con_auto.isChecked():
            report.append("active_con on\n")

        if self.checkBox_net_con_auto.isChecked():
            report.append("net_con on\n")

        if self.checkBox_brandmayer_auto.isChecked():
            report.append("brandmayer on\n")

        if self.checkBox_antivirus_auto.isChecked():
            report.append("antivirus on\n")

        if self.checkBox_process_auto.isChecked():
            report.append("process on\n")

        if self.checkBox_telegram_auto.isChecked():
            report.append(f"telegram on {self.lineEdit_tele_id.text().strip()}\n")

        source_monitor = "system_monitor.exe"
        source_scan_vuln = "scan_vuln_auto"
        if self.checkBox_autostart_auto.isChecked():
            report.append("autostart on")
            try:
                shutil.move("bg\\" + source_monitor, destination)
                shutil.move("bg\\" + source_scan_vuln, destination)
                print(f"Файл {source_monitor} перемещен!")
            except Exception as e:
                print("Ошибка: ", e)
        else:
            try:
                shutil.move(os.path.join(destination, source_monitor), os.getcwd() + "\\bg")
                shutil.move(os.path.join(destination, source_scan_vuln), os.getcwd() + "\\bg")
                print(f"Файл {source_monitor} перемещен!")
            except Exception as e:
                print("Ошибка: ", e)

        for item in report:
            print(item)

        string = "".join(report)

        with open('parameters.txt', "w", encoding="utf-8") as file:
            file.write(string)
        print(f"📝Файл обновлён!")

        # Если файл уже существует, удаляем его
        exist_parameters = os.path.join(destination, source_parameters)
        if os.path.exists(exist_parameters):
            os.remove(exist_parameters)
        shutil.move(source_parameters, destination) # Перемещаем файл

        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def set_file(self):
        from PyQt5.QtWidgets import QFileDialog

        file, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt) files (*.*)")
        print(file)
        self.lineEdit_send_file.setText(file)

    def send_tele(self):
        if os.path.isfile(self.lineEdit_send_file.text()):
            from tele_bot import telebot_send

            telebot_send.send_file_to_telegram(self.lineEdit_send_file.text())
            self.textBrowser_errors_send.setStyleSheet("color: green;")
            self.textBrowser_errors_send.setText(f"✅ Файл {self.lineEdit_send_file.text()} успешно отправлен!")
        else:
            self.textBrowser_errors_send.setStyleSheet("color: red;")
            self.textBrowser_errors_send.setText("❌ Такого файла не существует, введите правильный путь!")

    def save_chat_id(self):
        """Сохраняет текст из QLineEdit в файл"""
        text = self.lineEdit_tele_id.text().strip()
        try:
            with open('tele_bot\\chat_id.txt', "w", encoding="utf-8") as file:
                file.write(text)
            print(f"✅ Чат ID {text} успешно сохранен!")
            self.textBrowser_errors_send.setStyleSheet("color: green;")
            self.textBrowser_errors_send.setText(f"✅ Чат ID {text} успешно сохранен!")
        except Exception as e:
            print(f"Ошибка сохранения файла: {e}")
            self.textBrowser_errors_send.setStyleSheet("color: red;")
            self.textBrowser_errors_send.setText(f"❌Ошибка сохранения файла: {e}")

    def on_button_create_info(self):
        import subprocess
        from datetime import datetime

        QApplication.setOverrideCursor(Qt.WaitCursor)
        report = []

        if self.checkBox_port.isChecked():
            from scan_vuln import scan_top_ports

            report.append("=== Open Ports ===\n")
            self.textBrowser_errors_info.append("✅Open Ports")
            scan_ports = scan_top_ports.scan_common_ports()
            report.append(scan_ports)

        if self.checkBox_sys_info.isChecked():
            report.append("\n=== System Information ===\n")
            self.textBrowser_errors_info.append("✅System Information")
            sys_info = subprocess.check_output("systeminfo", shell=True, text=True, encoding="cp866")
            report.append(sys_info)

        if self.checkBox_active_con.isChecked():
            from scan_vuln import get_active_connections

            report.append("\n=== Active Connections ===")
            self.textBrowser_errors_info.append("✅Active Connections")
            active_connections = get_active_connections.get_active_connections()
            for conn in active_connections:
                report.append(f"Local: {conn['Local Address']} -> Remote: {conn['Remote Address']} (Status: {conn['Status']})")

        if self.checkBox_net_con.isChecked():
            from scan_vuln import get_network_info

            report.append("\n\n=== Network Information ===\n")
            self.textBrowser_errors_info.append("✅Network Information")
            network_info = get_network_info.get_network_info()
            for key, value in network_info.items():
                if key == "Interfaces":
                    report.append("Interfaces:")
                    for interface in value:
                        report.append(f"  - {interface['Interface']}: {interface['IP Address']} (Netmask: {interface['Netmask']})\n")
                else:
                    report.append(f"{key}: {value}")

        if self.checkBox_brandmayer.isChecked():
            import re

            report.append("\n=== Brandmayer Information ===\n")
            self.textBrowser_errors_info.append("✅Brandmayer Information")
            try:
                if re.search(r"State\s+OFF", subprocess.check_output("netsh advfirewall show allprofiles", shell=True).decode()):
                    report.append("[WARNING] Брандмауэр выключен!")
                else:
                    report.append("[OK] Брандмауэр включен.")
            except Exception as e:
                report.append(f"[ERROR] Ошибка проверки брандмауэра: {e}")

        if self.checkBox_antivirus.isChecked():
            from scan_vuln.check_antivirus import check

            report.append("\n\n=== Antivirus Information ===\n")
            self.textBrowser_errors_info.append("✅Antivirus Information")
            report.append(check)

        if self.checkBox_process.isChecked():
            from scan_vuln import process

            report.append("\n\n=== Process Information ===\n")
            self.textBrowser_errors_info.append("✅Process Information")
            report.append(process.get_process_report())

        for item in report:
            print(item)

        string = "".join(report)
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(string)
        print(f"📝Файл '{filename}' успешно создан и записан!")
        self.textBrowser_errors_info.append(f"📝Файл '{filename}' успешно создан и записан!")

        self.lineEdit_send_file.setText(filename)

        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def on_button_send_file(self):
        import socket
        import time
        from Crypto.Cipher import AES

        UDP_PORT = 37021
        TCP_PORT = 5002
        FILE_PATH = self.lineEdit_send_file.text()
        KEY = b'Sixteen byte key'  # 16-байтный ключ AES
        IV = b'This is an IV456'  # 16-байтный IV (инициализационный вектор)

        def encrypt_file(input_file):
            try:
                """ Функция шифрования файла """
                cipher = AES.new(KEY, AES.MODE_CFB, IV)

                with open(input_file, 'rb') as f:
                    file_data = f.read()

                encrypted_data = cipher.encrypt(file_data)
                return encrypted_data
            except Exception as e:
                print(f"Ошибка: {e}")

        def send_file(server_ip):
            tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_sock.connect((server_ip, TCP_PORT))
            print(f"[TCP] Подключение к серверу {server_ip}:{TCP_PORT}")
            try:
                encrypted_data = encrypt_file(FILE_PATH)
                tcp_sock.sendall(encrypted_data)
                print(f"🔐 Файл {FILE_PATH} зашифрован и отправлен!")
                self.textBrowser_errors_send.setStyleSheet("color: green;")
                self.textBrowser_errors_send.setText(f"✅ [UDP] Сервер найден по IP: {server_ip}🔐 Файл {FILE_PATH} зашифрован и отправлен!")

            except Exception as e:
                print(f"Ошибка при отправке файла: {e}")
            finally:
                tcp_sock.close()

        def discover_server_ip():
            udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            udp_sock.settimeout(5)

            print("[UDP] Отправка широковещательного запроса...")
            udp_sock.sendto(b"DISCOVER_SERVER", ('<broadcast>', UDP_PORT))

            try:
                data, addr = udp_sock.recvfrom(1024)
                server_ip = data.decode()
                print(f"[UDP] Сервер найден по IP: {server_ip}")
                return server_ip
            except socket.timeout:
                print("[UDP] Сервер не найден.")
                self.textBrowser_errors_send.setStyleSheet("color: red;")
                self.textBrowser_errors_send.setText(f"❌ [UDP] Сервер не найден.")
                return None

        QApplication.setOverrideCursor(Qt.WaitCursor)
        if os.path.isfile(FILE_PATH):
            server_ip = discover_server_ip()
            if server_ip:
                time.sleep(1)  # Даем серверу время подготовиться
                send_file(server_ip)
        else:
            self.textBrowser_errors_send.setStyleSheet("color: red;")
            self.textBrowser_errors_send.setText("❌ Такого файла не существует, введите правильный путь!")    
        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def toggle_timer(self, state):
            """Включение или отключение таймера при изменении состояния галочки."""
            if state == QtCore.Qt.Checked:
                self.timer.start(self.current_interval)  # Запускаем таймер с выбранным интервалом
            else:
                self.timer.stop()  # Останавливаем таймер

    def change_interval(self):
            """Обновление интервала на основе выбранного значения из выпадающего списка."""
            selected_text = self.comboBox_time.currentText()
            self.current_interval = self.intervals[selected_text]
            if self.checkBox_auto_search.isChecked():  # Если таймер уже запущен, обновляем интервал
                self.timer.start(self.current_interval)

    def on_button_click_client(self):
        import socket

        UDP_PORT = 37020
        TIMEOUT = 5

        def discover_server():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(TIMEOUT)

            message = b"DISCOVER_SERVER"
            sock.sendto(message, ('<broadcast>', UDP_PORT))
            print("[UDP] Широковещательный запрос отправлен. Ожидаем ответ...")

            try:
                data, server_addr = sock.recvfrom(1024)
                if data.decode() == "SERVER_HERE":
                    print(f"[UDP] Сервер найден по IP: {server_addr[0]}")
                    server_ip = server_addr[0]
                    return server_ip
            except socket.timeout:
                print("[UDP] Время ожидания истекло. Сервер не найден.")
                return None

        self.counter += 1
        self.label_count_q.setText(f"📡Количество отправенных запросов: {str(self.counter)}")

        server_ip = discover_server()
        if server_ip:
            print(f"[✓] IP сервера: {server_ip}")
            self.checkBox_auto_search.setChecked(False)
            self.textBrowser_errors.setStyleSheet("color: green;")
            self.textBrowser_errors.setText(f"🖥Server IP: {server_ip}, ✅Response: SERVER_HERE")
        else:
            print("[✗] Сервер не ответил.")
            self.textBrowser_errors.setStyleSheet("color: red;")
            self.textBrowser_errors.setText("❌ Сервер не ответил.")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Ui()
    main_window.show()
    sys.exit(app.exec_())
