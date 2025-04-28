import sys
import socket
import threading

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QRegExp, QTimer
from PyQt5.QtGui import QRegExpValidator, QPixmap

from server_get_file import MyApp

# Загрузка UI-файла
try:
    Form, _ = uic.loadUiType("main.ui")
except Exception as e:
    print(f"❌Ошибка загрузки UI: {e}")
    sys.exit(1)

ip_client = None            # Глобальная переменная клиента, которая находится в функции listen_for_broadcast()
flag_find_client = False    # Флажок для поиска клиента, включается когда клиент ищется, и отключается когда найден
client_index = 1            # Индексации и расположение клиентов на карте сети

# Список с цветами для отображения красивого вывода списка найденных устройств
colors = ["red", "blue", "green", "purple", "orange", "pink", "black"]


def listen_for_broadcast(): # Поднятие сервера для поиска клиента. Возвращает переменные flag_find_client и ip_client
    global ip_client
    global flag_find_client
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 37020))  # порт под broadcast
    print("Сервер: ожидаю broadcast от клиента...")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Получен broadcast от {addr[0]}: {data.decode()}")
        ip_client = addr[0]  # Сохраняем IP клиента
        sock.sendto(b"SERVER_HERE", addr)
        break  # Если нужно только один раз получить IP, можно выйти

    sock.close()
    print(f"[✓] IP клиента: {ip_client}")
    flag_find_client = True
    print(flag_find_client)


def is_connected(host="8.8.8.8", port=53, timeout=3):   # Наличие интернета
    """
    Проверяет наличие интернета, пытаясь подключиться к DNS серверу Google.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(f"Нет подключения к интернету: {ex}")
        return False


class Ui(QtWidgets.QMainWindow, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.progressBar.setValue(0)

        self.pushButton_scanner_ip.clicked.connect(self.on_button_click_scanner_ip)
        self.pushButton_list_port.clicked.connect(self.on_button_click_list_port)
        self.pushButton_ftp.clicked.connect(self.on_button_click_ftp)
        self.pushButton_ssh.clicked.connect(self.on_button_click_ssh)

        self.checkBox_find_client.stateChanged.connect(self.on_checkbox_find_client)
        self.server_thread = None

        self.pushButton_get_file.clicked.connect(self.on_checkbox_get_file)

        #255,255,255,255 регулярные выражения
        ip_regex = QRegExp(r"^(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\."
                           r"(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\."
                           r"(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\."
                           r"(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)$")
        # Устанавливаем валидатор
        validator = QRegExpValidator(ip_regex)
        self.lineEdit_brute_ip.setValidator(validator)
        self.lineEdit_ip_port_scan.setValidator(validator)

        for i in range(1, 13):
            label_pic = getattr(self, f"label_cli_{i}")
            label_pic.setText("")
            label_pic.clear()  # очищаем изображение, если было

            label_ip = getattr(self, f"label_online_client_{i}")
            label_ip.setText("")

    def check_client_ip(self):
        global flag_find_client

        if flag_find_client:
            self.checkBox_find_client.setChecked(False)
            self.label_client_ip.setText(f"💻IP клиента: {ip_client}")
            self.lineEdit_ip_port_scan.setText(ip_client)
            self.lineEdit_brute_ip.setText(ip_client)

            global client_index
            label_pic = getattr(self, f"label_cli_{client_index}")
            label_pic.setPixmap(QPixmap("img\\comp.png")) # Путь к изображению
            label_pic.setAlignment(Qt.AlignCenter)  # Центрируем изображение
            label_pic.setScaledContents(True)  # Масштабируем под размер QLabel

            label_ip = getattr(self, f"label_online_client_{client_index}")
            label_ip.setText(ip_client + "\nClient")
            label_ip.setStyleSheet("color: red;")
            client_index += 1
            flag_find_client = False
            self.timer_check_ip.stop()


    def on_checkbox_find_client(self, state):
        if self.checkBox_find_client.isChecked():
            self.server_thread = threading.Thread(target=listen_for_broadcast, daemon=True)
            self.server_thread.start()
            print("[i] Серверный поток запущен.")
            self.timer_check_ip = QTimer()
            self.timer_check_ip.timeout.connect(self.check_client_ip)
            self.timer_check_ip.start(5000)
        else:
            print("[i] Сервер не активен.")
            self.timer_check_ip.stop()


    def on_checkbox_get_file(self):
        self.server_ui = MyApp()
        self.server_ui.show()


    def on_button_click_scanner_ip(self):
        from scripts.get_ip_address_of_wifi import get_active_wifi_ip   # Ваш IP-адрес

        address = get_active_wifi_ip() # Ваш IP-адрес
        global label_pic
        global label_ip
        global client_index

        client_index = 1 # С каждым нажатием кнопки возвращаем индекс в изначальное положение

        # Очищение окон выводов данных, так как это списки
        self.textBrowser_ip_list.clear()
        self.textBrowser_mac_list.clear()
        self.textBrowser_name_comp_list.clear()
        for i in range(1, 13):
            label_pic = getattr(self, f"label_cli_{i}")
            label_pic.clear()  # Очищаем картинку
            label_pic.setText("")  # На всякий случай чистим текст тоже
            label_pic.setStyleSheet("")  # Сбрасываем стили (если хочешь)

            label_ip = getattr(self, f"label_online_client_{i}")
            label_ip.clear()  # Очищаем текст IP
            label_ip.setStyleSheet("")  # Сбрасываем стиль цвета

        if address:
            # Процесс обработки (типа прогрузка)
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.setWindowTitle("Сканирование...")
            self.progressBar.setValue(0)  # Сброс прогресса
            self.progressBar.setMaximum(100)
            self.start_progress()

            try:
                from scripts.router_ip import ip_router  # Default Gateway
                import requests
                import scapy.all as sc

                self.label_your_ip.setText(f"💻Ваш IP-адрес: {address}")
                self.label_server.setPixmap(QPixmap("img\\server.png"))  # Путь к изображению
                self.label_server.setAlignment(Qt.AlignCenter)  # Центрируем изображение
                self.label_server.setScaledContents(True)  # Масштабируем под размер QLabel
                self.label_online_server.setText(address)
                self.label_online_server.setStyleSheet("color: purple;")

                self.label_router_ip.setText("🖥Default Gateway: " + ip_router)
                self.label_router.setPixmap(QPixmap("img\\router.png"))  # Путь к изображению
                self.label_router.setAlignment(Qt.AlignCenter)  # Центрируем изображение
                self.label_router.setScaledContents(True)  # Масштабируем под размер QLabel
                self.label_online_router.setText(ip_router)
                self.label_online_router.setStyleSheet("color: orange;")

                if is_connected():
                    print("Интернет доступен!")
                    self.label_inter.setPixmap(QPixmap("img\\cloud.png")) # Путь к изображению
                    self.label_inter.setAlignment(Qt.AlignCenter)  # Центрируем изображение
                    self.label_inter.setScaledContents(True)  # Масштабируем под размер QLabel
                    self.label_internet.setText("Internet Connection is on")
                    self.label_internet.setStyleSheet("color: blue;")
                else:
                    print("Интернет недоступен.")
                    self.label_internet.setText("Internet Connection is off")
                    self.label_internet.setStyleSheet("color: red;")

                subnet = str(address + "/24")

                arp_request = sc.ARP(pdst=subnet)
                broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")
                arp_request_broadcast = broadcast / arp_request
                answered_list = sc.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

                devices = []

                for sent, received in answered_list:
                    response = requests.get(f"https://api.macvendors.com/{received.hwsrc}")
                    if response.status_code == 200:
                        manufac = response.text
                    else:
                        manufac = "Неизвестный производитель"
                    devices.append({"IP": received.psrc, "MAC": received.hwsrc, "Производитель": manufac})

                index = 0  # Индекс цвета

                for device in devices:
                    if device["IP"] != ip_router and device["IP"] != address:
                        color = colors[index % len(colors)]  # Меняем цвет циклически
                        self.textBrowser_ip_list.append(f'<span style="color:{color};">{device["IP"]}</span>')
                        self.textBrowser_mac_list.append(f'<span style="color:{color};">{device["MAC"]}</span>')
                        self.textBrowser_name_comp_list.append(f'<span style="color:{color};">{device["Производитель"]}</span>')

                        label_pic = getattr(self, f"label_cli_{client_index}")
                        label_pic.setPixmap(QPixmap("img\\comp.png")) # Путь к изображению
                        label_pic.setAlignment(Qt.AlignCenter)  # Центрируем изображение
                        label_pic.setScaledContents(True)  # Масштабируем под размер QLabel

                        label_ip = getattr(self, f"label_online_client_{client_index}")
                        label_ip.setText(device["IP"])
                        label_ip.setStyleSheet("color: green;")

                        index += 1  # Переход к следующему цвету
                        client_index += 1  # <- увеличиваем счётчик

                devices.clear()

                self.textBrowser_errors.setStyleSheet("color: green;")
                self.textBrowser_errors.setText("✅Сканирование завершено")
                print("✅Сканирование завершено")

            except Exception as e:
                self.textBrowser_errors.setStyleSheet("color: red;")
                self.textBrowser_errors.setText(f"❌ Ошибка: {e}")
                print(f"❌ Ошибка: {e}")

            #Прогрузка завершена
            self.progressBar.setValue(100)
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.setWindowTitle("CompSecMonSys - Administator")

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Подключение к Wi-Fi")
            msg.setText("Пожалуйста, подключитесь к Wi-Fi сети для продолжения работы и перезагрузите программу.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()


    def on_button_click_list_port(self):
        import scripts.scaner_of_ip_port

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

                ports_list = scripts.scaner_of_ip_port.scan_common_ports(self.lineEdit_ip_port_scan.text()).split("\n")
                for i in ports_list:
                    if "открыт" in i:
                        self.textBrowser_list_port.append(f'<span style="color:green;">{i}</span>')
                    else:
                        self.textBrowser_list_port.append(f'<span style="color:red;">{i}</span>')
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
        import os
        from scripts import ftp_brute

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
        from scripts import ssh_brute

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
        import random
        import time

        # Обновляем progressBar с задержкой
        for value in range(0, random.randint(50, 90), 1):  # От 0 до 100 с шагом 10
            self.progressBar.setValue(value)  # Устанавливаем значение
            time.sleep(random.uniform(0.01, 0.1))  # Задержка в 0.1 секунды


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Ui()
    main_window.show()
    sys.exit(app.exec_())
