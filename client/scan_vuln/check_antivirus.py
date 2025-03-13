import subprocess

def check_antivirus():
    try:
        # Выполняем команду PowerShell для получения списка антивирусов
        command = 'powershell "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | Select-Object displayName"'
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Извлекаем строки с названиями антивирусов
        output = result.stdout.strip().split("\n")[2:]  # Пропускаем заголовки

        # Выводим список антивирусов, если найдены
        antivirus_list = [line.strip() for line in output if line.strip()]
        
        if antivirus_list:
            for av in antivirus_list:
                return f"[OK] {av}"
        else:
            return "[WARNING] Антивирус не найден!"

    except Exception as e:
        print(f"Ошибка при проверке антивируса: {e}")

check = check_antivirus()