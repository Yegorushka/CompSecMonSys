import socket

# Список часто используемых портов, которые могут быть подвержены уязвимостям
common_ports = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    135: 'RPC',
    139: 'NetBIOS',
    143: 'IMAP',
    443: 'HTTPS',
    445: 'SMB',
    3306: 'MySQL',
    3389: 'RDP'
}


def scan_port(ip, port, result_str):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)  # Установка тайм-аута
        result = sock.connect_ex((ip, port))
        if result == 0:
            status = f"Порт {port} ({common_ports[port]}) открыт\n"
        else:
            status = f"Порт {port} ({common_ports[port]}) закрыт\n"
        result_str.append(status)  # Добавляем строку в список
        sock.close()
    except Exception as e:
        error = f"Ошибка при сканировании порта {port}: {e}\n"
        result_str.append(error)


def scan_common_ports(ip="127.0.0.1"):
    # print(f"Сканирование хоста {ip} на наличие открытых общих портов...")
    port_scan_result = []  # Список для хранения строк
    for port in common_ports:
        scan_port(ip, port, port_scan_result)

    # Объединяем строки в одну строку
    final_result = ''.join(port_scan_result)
    return final_result
