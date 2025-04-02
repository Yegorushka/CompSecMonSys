# C:\Users\(x_x)\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

import re, subprocess, os, sys
from datetime import datetime

# path = os.getcwd()
# sys.path.append(path)
# with open(os.path.join(path, "parameters.txt"), "r", encoding="utf-8") as file:

report = []
with open(os.path.join(r"C:\Users\(x_x)\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup", 'parameters.txt'), "r", encoding="utf-8") as file:
    content = file.read().strip().lower()
print("open file")

if "ports on" in content:
    # Открытые порты
    from scan_vuln import scan_top_ports
    report.append("=== Open Ports ===\n")
    scan_ports = scan_top_ports.scan_common_ports()
    report.append(scan_ports)
    print("Open Ports")

if  "sys_info on" in content:
    # Системная информация
    from scan_vuln import get_system_info
    report.append("\n=== System Information ===\n")
    system_info = get_system_info.get_system_info()
    for key, value in system_info.items():
        report.append(f"{key}: {value}")
    print("System Information")

if  "active_con on" in content:
    # Активные соединения
    from scan_vuln import get_active_connections
    report.append("\n=== Active Connections ===\n")
    active_connections = get_active_connections.get_active_connections()
    for conn in active_connections:
        report.append(f"Local: {conn['Local Address']} -> Remote: {conn['Remote Address']} (Status: {conn['Status']})")
    print("Active Connections")

if  "net_con on" in content:
    # Сетевые интерфейсы
    from scan_vuln import get_network_info
    report.append("\n\n=== Network Information ===\n")
    network_info = get_network_info.get_network_info()
    for key, value in network_info.items():
        if key == "Interfaces":
            report.append("Interfaces:")
            for interface in value:
                report.append(f"  - {interface['Interface']}: {interface['IP Address']} (Netmask: {interface['Netmask']})\n")
        else:
            report.append(f"{key}: {value}")
    print("Network Information")

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
    print("Brandmayer Information")

if "antivirus on" in content:
    from scan_vuln.check_antivirus import check
    report.append("\n\n=== Antivirus Information ===\n")
    report.append(check)
    print("Antivirus Information")

if "vuln on" in content:
    from scan_vuln.check_windows_vulnerabilities import check
    report.append("\n\n=== Vulnerable Information ===\n")
    for x in check:
        report.append(x)
    print("Vulnerable Information")

if "process on" in content:
    from scan_vuln import process
    report.append("\n\n=== Process Information ===\n")
    report.append(process.get_process_report())
    print("Process Information\n")

string = "".join(report)
save_path = r'C:\Users\(x_x)\Documents'
file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
full_path = os.path.join(save_path, file_name)
with open(full_path, "w", encoding="utf-8") as file:
    file.write(string)
print("Finish!!!")