import psutil
from datetime import datetime

def get_process_report():
    """Функция собирает информацию о процессах и возвращает в виде строки"""
    processes = []
    for process in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent', 'exe']):
        try:
            processes.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # report = f"Отчет о процессах ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n"
    report = "=" * 80 + "\n"
    report += f"{'PID':<8}{'Процесс':<25}{'CPU %':<10}{'RAM %':<10}{'Исполняемый файл'}\n"
    report += "=" * 80 + "\n"

    for proc in processes:
        report += f"{proc['pid']:<8}{proc['name']:<25}{proc['cpu_percent']:<10}{proc['memory_percent']:<10}{proc.get('exe', 'N/A')}\n"

    return report

if __name__ == "__main__":
    result = get_process_report()
    print(result)  # Вывод отчета в консоль
