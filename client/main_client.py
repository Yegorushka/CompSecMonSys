from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import sys, os, socket, subprocess, re
from Crypto.Cipher import AES

try:
    Form, _ = uic.loadUiType("main_client.ui")
except Exception as e:
    print(f"❌Ошибка загрузки UI: {e}")
    sys.exit(1)

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
        self.current_interval = 5000  # Интервал по умолчанию: 1 секунда
        # Создаем таймер
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.on_button_click_client)  # Соединяем сигнал таймера с методом

        self.pushButton_create_info.clicked.connect(self.on_button_create_info)
        
        with open('scripts/telegram/chat_id.txt', "r", encoding="utf-8") as file:
            text = file.read().strip()
            self.lineEdit_tele_id.setText(text)
        
        self.pushButton_save_tele_id.clicked.connect(self.save_chat_id)
        self.pushButton_send_tele.clicked.connect(self.send_tele)
        self.pushButton_set_file.clicked.connect(self.set_file)

    def set_file(self):
        from PyQt5.QtWidgets import QFileDialog
        file, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt) files (*.*)")
        print(file)
        self.lineEdit_send_file.setText(file)

    def send_tele(self):
        if os.path.isfile(self.lineEdit_send_file.text()):
            from scripts import telebot_send
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
            with open('scripts\\telegram\\chat_id.txt', "w", encoding="utf-8") as file:
                file.write(text)
            print(f"✅ Чат ID {text} успешно сохранен!")
            self.textBrowser_errors_send.setStyleSheet("color: green;")
            self.textBrowser_errors_send.setText(f"✅ Чат ID {text} успешно сохранен!")
        except Exception as e:
            print(f"Ошибка сохранения файла: {e}") 
            self.textBrowser_errors_send.setStyleSheet("color: red;")
            self.textBrowser_errors_send.setText(f"❌Ошибка сохранения файла: {e}")

    def on_button_create_info(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        report = []
        if self.checkBox_port.isChecked():
            # Открытые порты
            from scan_vuln import scan_top_ports
            report.append("=== Open Ports ===")
            self.textBrowser_errors_info.append("✅Open Ports")
            scan_ports = scan_top_ports.scan_common_ports()
            report.append(scan_ports)

        if self.checkBox_sys_info.isChecked(): 
            # Системная информация
            from scan_vuln import get_system_info
            report.append("\n=== System Information ===\n")
            self.textBrowser_errors_info.append("✅System Information")
            system_info = get_system_info.get_system_info()
            for key, value in system_info.items():
                report.append(f"{key}: {value}")

        if self.checkBox_active_con.isChecked():
            # Активные соединения
            from scan_vuln import get_active_connections
            report.append("\n=== Active Connections ===")
            self.textBrowser_errors_info.append("✅Active Connections")
            active_connections = get_active_connections.get_active_connections()
            for conn in active_connections:
                report.append(f"Local: {conn['Local Address']} -> Remote: {conn['Remote Address']} (Status: {conn['Status']})")

        if self.checkBox_net_con.isChecked():
            # Сетевые интерфейсы
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
            """Проверка состояния брандмауэра"""
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

        if self.checkBox_vuln.isChecked():
            from scan_vuln.check_windows_vulnerabilities import check
            report.append("\n\n=== Vulnerable Information ===\n")
            self.textBrowser_errors_info.append("✅Vulnerable Information")
            for x in check:
                report.append(x)

        if self.checkBox_process.isChecked():
            from scan_vuln import process
            report.append("\n\n=== Process Information ===\n")
            self.textBrowser_errors_info.append("✅Process Information")
            report.append(process.get_process_report())

        for item in report:    
            print(item)

        string = "".join(report)
        from datetime import datetime
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(string)
        print(f"📝Файл '{filename}' успешно создан и записан!")
        self.textBrowser_errors_info.append(f"📝Файл '{filename}' успешно создан и записан!")

        self.lineEdit_send_file.setText(filename)

        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def on_button_send_file(self):

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

        def send_file(client_socket, filename):
            """ Отправка зашифрованного файла """
            try:
                encrypted_data = encrypt_file(filename)
                client_socket.sendall(encrypted_data)
                print(f"🔐 Файл {filename} зашифрован и отправлен!")
            except Exception as e:
                print(f"Ошибка при отправке файла: {e}")
            finally:
                client_socket.close()

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            if os.path.isfile(self.lineEdit_send_file.text()):                 
                try:
                    host = '0.0.0.0'  # Ожидает подключения на всех интерфейсах
                    port = 12346  

                    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_socket.bind((host, port))
                    server_socket.listen(1)
                    server_socket.settimeout(5)
                    print(f"📡 Сервер запущен на {host}:{port}, ожидаем подключение...")


                    client_socket, client_address = server_socket.accept()
                    print(f"✅ Подключено к {client_address}")

                    send_file(client_socket, self.lineEdit_send_file.text())

                    server_socket.close()

                    self.textBrowser_errors_send.setStyleSheet("color: green;")
                    self.textBrowser_errors_send.setText(f"✅ Подключено к {client_address}\n📤Файл отправлен!")

                except Exception as e:
                    print(f"Ошибка: {e}")
                    self.textBrowser_errors_send.setStyleSheet("color: red;")
                    self.textBrowser_errors_send.setText(f"Ошибка: {e}")

            else:
                self.textBrowser_errors_send.setStyleSheet("color: red;")
                self.textBrowser_errors_send.setText("❌ Такого файла не существует, введите правильный путь!")                
        except Exception as e:
            self.textBrowser_errors_send.setStyleSheet("color: red;")
            self.textBrowser_errors_send.setText(f"❌ Ошибка: {e}")
            print(f"Ошибка: {e}")
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
        from scripts import replace_last_octet_with_255
        from scripts import get_ip_address_of_wifi
        self.counter += 1
        self.label_count_q.setText(f"📡Количество отправенных запросов: {str(self.counter)}")
        ip_client = get_ip_address_of_wifi.get_ip_address_of_wifi()

        self.label_localhost.setText(f"💻Ваш IP-адрес: {ip_client}")
        print(f"💻Ваш IP-адрес: {ip_client}")
        try:

            broadcast_address = replace_last_octet_with_255.replace_last_octet_with_255(ip_client)
            print(broadcast_address)
            port = 12345
            message = b"Who is the server?"
            ip_server = ''

            # Настройка сокета для широковещательной передачи
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(message, (broadcast_address, port))

            # Ожидание ответа
            sock.settimeout(1)
            try:
                response, server_address = sock.recvfrom(1024)
                print(f"Server IP: {server_address[0]}, Response: {response.decode()}")
                ip_server = server_address[0]
            except socket.timeout:
                print("No response from server.")

            self.textBrowser_errors.setStyleSheet("color: green;")
            self.textBrowser_errors.setText(f"🖥Server IP: {server_address[0]}, ✅Response: {response.decode()}")

            # Настройка клиента
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip_server, 12345))  # Замените 'IP_сервера' на реальный IP адрес сервера

            # Отправка сообщений
            while True:
                # message = input("Введите сообщение: ")
                client_socket.send(ip_client.encode('utf-8'))

                # if message.lower() == 'exit':
                #     break

                response = client_socket.recv(1024).decode('utf-8')
                print(f"Ответ от сервера: {response}")
                break
            client_socket.close()

            self.timer.stop()
            self.checkBox_auto_search.setChecked(False)

        except Exception as e:
            self.textBrowser_errors.setStyleSheet("color: red;")
            self.textBrowser_errors.setText(f"❌ Ошибка: {e}")
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Ui()
    main_window.show()
    sys.exit(app.exec_())