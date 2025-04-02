import winreg

def remove_from_autostart():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                          r"Software\Microsoft\Windows\CurrentVersion\Run", 
                          0, winreg.KEY_SET_VALUE)
    winreg.DeleteValue(key, "SystemMonitor")
    winreg.CloseKey(key)
    print("Программа удалена из автозапуска!")

remove_from_autostart()
