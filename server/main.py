from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from Crypto.Cipher import AES
from datetime import datetime
import sys, time, os, random, socket

from scripts import ftp_brute, ssh_brute
# Загрузка UI-файла
try:
    Form, _ = uic.loadUiType("main.ui")
except Exception as e:
    print(f"❌Ошибка загрузки UI: {e}")
    sys.exit(1)

import scripts.scaner_of_ip_port
ip_client = ''

class Ui(QtWidgets.QMainWindow, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)

        self.pushButton_scanner_ip.clicked.connect(self.on_button_click_scanner_ip)
        self.pushButton_find_client.clicked.connect(self.on_button_click_find_client)
        self.pushButton_list_port.clicked.connect(self.on_button_click_list_port)
        self.pushButton_ftp.clicked.connect(self.on_button_click_ftp)
        self.pushButton_ssh.clicked.connect(self.on_button_click_ssh)

        self.progressBar.setValue(0)

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
        self.timer.timeout.connect(self.on_button_get_file)  # Соединяем сигнал таймера с методом
        
        ip_regex = QRegExp(r"^(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\."
                           r"(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\."
                           r"(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\."
                           r"(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)$")
        
        # Устанавливаем валидатор
        validator = QRegExpValidator(ip_regex)
        self.lineEdit_brute_ip.setValidator(validator)
        self.lineEdit_ip_port_scan.setValidator(validator)
        self.lineEdit_ip_get_file.setValidator(validator)

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

    def on_button_get_file(self):
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
                self.textBrowser_errors_get.setStyleSheet("color: green;")
                self.textBrowser_errors_get.setText(f"🔓 Файл успешно получен и расшифрован -> {save_path}")
            except Exception as e:
                print(f"Ошибка при получении файла: {e}")
            finally:
                server_socket.close()
        if self.lineEdit_ip_get_file.text() == '':
            self.textBrowser_errors_get.setStyleSheet("color: red;")
            self.textBrowser_errors_get.setText("🖥Введите IP-адрес клиента, от которого будет получен файл")
            self.timer.stop()
            self.checkBox_auto_search.setChecked(False)
        else:
            try:
                if self.lineEdit_ip_get_file.text() == "":
                    print("🖥Введите IP-адрес клиента, от которого будет получен файл")
                    self.textBrowser_errors_get.setStyleSheet("color: red;")
                    self.textBrowser_errors_get.setText("🖥Введите IP-адрес клиента, от которого будет получен файл")
                else:  
                    # ip_client = '192.168.2.101'  # IP сервера
                    print(self.lineEdit_ip_get_file.text())
                    port = 12346

                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((self.lineEdit_ip_get_file.text(), port))

                    receive_file(client_socket, now.strftime("%Y-%m-%d_%H-%M-%S")+'.txt')

                    self.timer.stop()
                    self.checkBox_auto_search.setChecked(False)

            except Exception as e:
                self.textBrowser_errors_get.setStyleSheet("color: red;")
                self.textBrowser_errors_get.setText(f"❌ Ошибка: {e}")
                print(f"Ошибка: {e}")

    def on_button_click_scanner_ip(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            # self.textBrowser_errors.setText("")
            # self.progressBar.setValue(0)  # Сброс прогресса
            # self.progressBar.setMaximum(100)
            # self.start_progress()

            from scripts.get_ip_address_of_wifi import address
            from scripts.router_ip import ip_router
            self.label_your_ip.setText(f"💻Ваш IP-адрес: {address}")
            self.label_router_ip.setText("🖥Default Gateway: " + ip_router)
            
            subnet = str(address + "/24")
            # subnet = address.rsplit('.',1)[0]
            # import scripts.scanner_of_ip
            # available_ips = scripts.scanner_of_ip.scan_network(subnet)

            import scapy.all as sc
            arp_request = sc.ARP(pdst=subnet)
            broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            answered_list = sc.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

            devices = []
            import requests
           
            for sent, received in answered_list:
                response = requests.get(f"https://api.macvendors.com/{received.hwsrc}")
                if response.status_code == 200:
                    manufac = response.text
                else:
                    manufac = "Неизвестный производитель"
                devices.append({"IP": received.psrc, "MAC": received.hwsrc, "Производитель": manufac})

            for device in devices:
                # if device == ip_router:
                #     print(f"IP: {device['IP']} - MAC: {device['MAC']} 🖥Default Gateway")
                #     self.textBrowser_ip_list.append(f"IP: {device['IP']} - MAC: {device['MAC']} (🖥Default Gateway)")  # Изменяем текст на метке
                #     continue

                # if device == address:
                #     print(f"IP: {device['IP']} - MAC: {device['MAC']} 💻Твой IP-адрес")
                #     self.textBrowser_ip_list.append(f"IP: {device['IP']} - MAC: {device['MAC']} (💻Ваш IP-адрес)")  # Изменяем текст на метке
                #     continue   
                # print(device)
                self.textBrowser_ip_list.append(f"IP: {device['IP']} - MAC: {device['MAC']} - Производитель: {device['Производитель']}")  # Изменяем текст на метке

            self.textBrowser_errors.setStyleSheet("color: green;")
            self.textBrowser_errors.setText("✅Сканирование завершено")
            print("✅Сканирование завершено")

            
        except Exception as e:
            self.textBrowser_errors.setStyleSheet("color: red;")
            self.textBrowser_errors.setText(f"❌ Ошибка: {e}")
            print(f"❌ Ошибка: {e}")
            # sys.exit(1)

        # self.progressBar.setValue(100)
        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def on_button_click_find_client(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.textBrowser_errors.setText("")
            # self.progressBar.setValue(0)  # Сброс прогресса
            # self.progressBar.setMaximum(100)
            # self.start_progress()
            
            from scripts.server import ip_address
            self.label_client_ip.setText(f"💻IP клиента: {ip_address}")
            self.lineEdit_ip_port_scan.setText(ip_address)
            self.lineEdit_brute_ip.setText(ip_address)
            self.lineEdit_ip_get_file.setText(ip_address)
            global ip_client
            ip_client = ip_address
        except Exception as e:
            self.textBrowser_errors.setStyleSheet("color: red;")
            self.textBrowser_errors.setText(f"❌ Ошибка: {e}")
            print(f"❌ Ошибка: {e}")
            # sys.exit(1)

        # self.progressBar.setValue(100)
        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def on_button_click_list_port(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.textBrowser_errors.setText("")
            global ip_client
            if ip_client != '' and self.lineEdit_ip_port_scan.text() == '':
                self.progressBar.setValue(0)  # Сброс прогресса
                self.progressBar.setMaximum(100)
                self.start_progress()
                self.textBrowser_list_port.setText(scripts.scaner_of_ip_port.scan_common_ports(ip_client))
            elif self.lineEdit_ip_port_scan.text() != '':
                self.progressBar.setValue(0)  # Сброс прогресса
                self.progressBar.setMaximum(100)
                self.start_progress()
                self.textBrowser_list_port.setText(scripts.scaner_of_ip_port.scan_common_ports(self.lineEdit_ip_port_scan.text()))
            else:
                print("Ошибка: введите IP-адрес цели для сканирование портов")
                self.textBrowser_errors.setStyleSheet("color: red;")
                self.textBrowser_errors.setText("Ошибка: введите IP-адрес цели для сканирование портов")
        except Exception as e:
            print(ip_client)
            self.textBrowser_errors.setStyleSheet("color: red;")
            self.textBrowser_errors.setText(f"❌ Ошибка: {e}")
            print(f"❌ Ошибка: {e}")
            # sys.exit(1)

        self.progressBar.setValue(100)
        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def on_button_click_ftp(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.textBrowser_errors.setText("")
            
            
            if self.lineEdit_brute_ip.text() == "":
                self.textBrowser_errors.setStyleSheet("color: red;")
                self.textBrowser_errors.setText("Ошибка: введите IP-адрес цели")
                print("введите IP-адрес цели")

            elif self.lineEdit_brute_ip.text() != "":
                if self.lineEdit_brute_file.text() == "":         
                    self.textBrowser_brute.setText(ftp_brute.ftp_bruteforce(self.lineEdit_brute_ip.text(), 'pwlist\\password.txt'))
                    print(self.lineEdit_brute_ip.text() + " " + 'pwlist\\password.txt')
                else:
                    if os.path.isfile(self.lineEdit_brute_file.text()):
                        print(f"Файл найден: " + self.lineEdit_brute_file.text())
                        print(self.lineEdit_brute_ip.text() + " " + self.lineEdit_brute_file.text())
                        self.textBrowser_brute.setText(ftp_brute.ftp_bruteforce(self.lineEdit_brute_ip.text(), self.lineEdit_brute_file.text()))
                    else:
                        print(f"Файл не найден: "+ self.lineEdit_brute_file.text() +". Попробуйте еще раз или оставьте строку пустой")
            else:
                print("err")
        except Exception as e:
            self.textBrowser_errors.setStyleSheet("color: red;")
            self.textBrowser_errors.setText(f"❌ Ошибка: {e}")
            print(f"❌ Ошибка: {e}")
        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def on_button_click_ssh(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.textBrowser_errors.setText("")
            global ip_client
            path = 'pwlist\\password.txt'

            if self.lineEdit_brute_ip.text() == "":
                self.textBrowser_errors.setStyleSheet("color: red;")
                self.textBrowser_errors.setText("Ошибка: введите IP-адрес цели")
                print(self.lineEdit_brute_ip.text() + " " + ip_client)
                print("введите IP-адрес цели")

            elif self.lineEdit_brute_ip.text().strip() != "":
                if self.lineEdit_brute_file.text().strip() == "":         
                    self.textBrowser_brute.setText(ssh_brute.check_ssh_login(ip_client, path))
                    print(self.lineEdit_brute_ip.text() + " " + path)
                else:
                    print(self.lineEdit_brute_ip.text() + " " + self.lineEdit_brute_file.text())
                    self.textBrowser_brute.setText(ssh_brute.check_ssh_login(self.lineEdit_brute_ip.text(), self.lineEdit_brute_file.text()))
            else:
                print("err")
        except Exception as e:
            self.textBrowser_errors.setStyleSheet("color: red;")
            self.textBrowser_errors.setText(f"❌ Ошибка: {e}")
            print(f"❌ Ошибка: {e}")
        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def start_progress(self):
        # Обновляем progressBar с задержкой
        for value in range(0, random.randint(50, 90), 1):  # От 0 до 100 с шагом 10
            self.progressBar.setValue(value)  # Устанавливаем значение
            time.sleep(random.uniform(0.01, 0.1))  # Задержка в 0.5 секунды

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Ui()
    main_window.show()
    sys.exit(app.exec_())
