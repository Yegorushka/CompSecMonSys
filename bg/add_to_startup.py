import os
import sys
import winreg

def add_to_autostart():
    script_path = os.path.abspath("system_monitor.exe")  # Указываем путь к основному файлу
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                          r"Software\Microsoft\Windows\CurrentVersion\Run", 
                          0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "SystemMonitor", 0, winreg.REG_SZ, script_path)
    winreg.CloseKey(key)
    print("Программа добавлена в автозапуск!")

add_to_autostart()
