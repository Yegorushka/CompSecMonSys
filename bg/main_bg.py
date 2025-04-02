from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import sys, os, shutil, socket

try:
    Form, _ = uic.loadUiType("bg.ui")
except Exception as e:
    print(f"❌Ошибка загрузки UI: {e}")
    sys.exit(1)

destination = r"C:\Users\(x_x)\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
source_parameters = 'parameters.txt'

class Ui(QtWidgets.QMainWindow, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)

        self.pushButton_save.clicked.connect(self.on_button_create_info)
        self.checkBox_autostart.stateChanged.connect(self.toggle_text_checkbox)
        self.load_checkbox_state()

    def load_checkbox_state(self):
        """Читает файл и устанавливает состояние чекбокса"""
        path_parameters = os.path.join(destination, source_parameters)
        if os.path.exists(path_parameters):
            with open(path_parameters, "r", encoding="utf-8") as file:
                content = file.read().strip().lower()
                if "autostart on" in content:
                    self.checkBox_autostart.setChecked(True)  # Включаем чекбокс
                    self.checkBox_autostart.setText("Включенный автозапуск")
                else:
                    self.checkBox_autostart.setChecked(False)  # Выключаем чекбокс
                    self.checkBox_autostart.setText("Выключенный автозапуск")
        else:
            self.checkBox_autostart.setChecked(False)  # Если файла нет, чекбокс выключен
            self.checkBox_autostart.setText("Выключенный автозапуск")

    def toggle_text_checkbox(self, state):
        """Меняет текст чекбокса при активации/деактивации"""
        if state == 2:  # Qt.Checked
            self.checkBox_autostart.setText("Включенный автозапуск")
        else:
            self.checkBox_autostart.setText("Выключенный автозапуск")

    def on_button_create_info(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        report = []

        # Я не могу использовать это, так как мое имя содержит скобки, а  os.path.join выводит его без скобок
        # destination = os.path.join(
        #     "C:\\Users", socket.gethostname(), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
        # ) 

        if self.checkBox_port.isChecked():
            report.append("ports on\n")

        if self.checkBox_sys_info.isChecked(): 
            report.append("sys_info on\n")

        if self.checkBox_active_con.isChecked():
            report.append("active_con on\n")

        if self.checkBox_net_con.isChecked():
            report.append("net_con on\n")

        if self.checkBox_brandmayer.isChecked():
            report.append("brandmayer on\n")

        if self.checkBox_antivirus.isChecked():
            report.append("antivirus on\n")

        if self.checkBox_vuln.isChecked():
            report.append("vuln on\n")

        if self.checkBox_process.isChecked():
            report.append("process on\n")

        source_monitor = "system_monitor.py"
        source_scan_vuln = "scan_vuln"
        if self.checkBox_autostart.isChecked():
            report.append("autostart on")
            try:
                shutil.move(source_monitor, destination) # Перемещаем файл
                shutil.move(source_scan_vuln, destination)
                print(f"Файл {source_monitor} перемещен!")
            except Exception as e:
                print("Ошибка: ",e)
        else:
            try:
                shutil.move(os.path.join(destination, source_monitor), os.getcwd())
                shutil.move(os.path.join(destination, source_scan_vuln), os.getcwd())
                print(f"Файл {source_monitor} перемещен!")
            except Exception as e:
                print("Ошибка: ",e)

        for item in report:    
            print(item)

        string = "".join(report)
        from datetime import datetime
        with open('parameters.txt', "w", encoding="utf-8") as file:
            file.write(string)
        print(f"📝Файл обновлён!")

        # destination = r"C:\Users\(x_x)\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\parameters.txt"
  

        # Если файл уже существует, удаляем его
        exist_parameters = os.path.join(destination, source_parameters)
        if os.path.exists(exist_parameters):
            os.remove(exist_parameters)
        shutil.move(source_parameters, destination) # Перемещаем файл

        QApplication.setOverrideCursor(Qt.ArrowCursor)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Ui()
    main_window.show()
    sys.exit(app.exec_())