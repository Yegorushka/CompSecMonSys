# C:\Users\(x_x)\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

import re
import subprocess
import os
from datetime import datetime

report = []
destination = os.path.join("C:\\Users", os.getlogin(), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup") 
with open(os.path.join(destination, 'parameters.txt'), "r", encoding="utf-8") as file:
    content = file.read().strip().lower()
# print("open file")

if "ports on" in content:
    # Открытые порты
    from scan_vuln_auto import scan_top_ports
    report.append("=== Open Ports ===\n")
    scan_ports = scan_top_ports.scan_common_ports()
    report.append(scan_ports)
    # print("Open Ports")

if "sys_info on" in content:
    report.append("\n=== System Information ===")
    sys_info = subprocess.check_output("systeminfo", shell=True, text=True, encoding="cp866")
    report.append(sys_info)

if "active_con on" in content:
    # Активные соединения
    from scan_vuln_auto import get_active_connections
    report.append("\n=== Active Connections ===\n")
    active_connections = get_active_connections.get_active_connections()
    for conn in active_connections:
        report.append(f"Local: {conn['Local Address']} -> Remote: {conn['Remote Address']} (Status: {conn['Status']})")

if "net_con on" in content:
    # Сетевые интерфейсы
    from scan_vuln_auto import get_network_info
    report.append("\n\n=== Network Information ===\n")
    network_info = get_network_info.get_network_info()
    for key, value in network_info.items():
        if key == "Interfaces":
            report.append("Interfaces:")
            for interface in value:
                report.append(f"  - {interface['Interface']}: {interface['IP Address']} (Netmask: {interface['Netmask']})\n")
        else:
            report.append(f"{key}: {value}")

if "brandmayer on" in content:
    """Проверка состояния брандмауэра"""
    report.append("\n=== Brandmayer Information ===\n")
    try:
        if re.search(r"State\s+OFF", subprocess.check_output("netsh advfirewall show allprofiles", shell=True).decode()):
            report.append("[WARNING] Брандмауэр выключен!")
        else:
            report.append("[OK] Брандмауэр включен.")
    except Exception as e:
        report.append(f"[ERROR] Ошибка проверки брандмауэра: {e}")

if "antivirus on" in content:
    from scan_vuln_auto.check_antivirus import check
    report.append("\n\n=== Antivirus Information ===\n")
    report.append(check)

if "process on" in content:
    from scan_vuln_auto import process
    report.append("\n\n=== Process Information ===\n")
    report.append(process.get_process_report())

string = "".join(report)
save_path = os.path.join("C:\\Users", os.getlogin(), "Documents")
file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
full_path = os.path.join(save_path, file_name)
with open(full_path, "w", encoding="utf-8") as file:
    file.write(string)

if "telegram on" in content:
    from scan_vuln_auto import telebot_send
    match = re.search(r"telegram on (\d+)", content)
    telebot_send.send_file_to_telegram(full_path, match.group(1))
