import subprocess

def check_windows_vulnerabilities():
    report = []
    try:
        # Проверка наличия критических обновлений безопасности
        command_updates = 'powershell "Get-HotFix | Where-Object {$_.Description -eq \'Security Update\'} | Select-Object HotFixID, InstalledOn"'
        result_updates = subprocess.run(command_updates, capture_output=True, text=True, shell=True)
        
        # Проверка устаревших компонентов (например, SMBv1)
        command_smbv1 = 'powershell "Get-WindowsOptionalFeature -Online | Where-Object {$_.FeatureName -like \'SMB1Protocol\'}"'
        result_smbv1 = subprocess.run(command_smbv1, capture_output=True, text=True, shell=True)
        
        # Проверка устаревших драйверов
        command_drivers = 'wmic qfe get HotFixID, InstalledOn'
        result_drivers = subprocess.run(command_drivers, capture_output=True, text=True, shell=True)

        # Вывод результатов
        report.append("[!] Установленные обновления безопасности:")
        report.append(result_updates.stdout.strip() if result_updates.stdout.strip() else "❌ Нет установленных обновлений безопасности!")

        report.append("\n[!] Проверка устаревших компонентов:")
        if "Enabled" in result_smbv1.stdout:
            report.append("[!] Включен протокол SMBv1 (уязвим!)")
        else:
            report.append("[OK] Протокол SMBv1 отключен (безопасно)")

        report.append("\n[!] Проверка установленных обновлений (через WMIC):")
        report.append(result_drivers.stdout.strip() if result_drivers.stdout.strip() else "❌ Информация недоступна")

        return report

    except Exception as e:
        report.append(f"❌ Ошибка при проверке уязвимостей: {e}")
        return report

# Запускаем проверку
check = check_windows_vulnerabilities()
