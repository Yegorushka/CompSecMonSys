import psutil
import socket


def get_network_info():
    network_info = {}
    net_io = psutil.net_io_counters()
    network_info['Bytes Sent'] = f"{net_io.bytes_sent / (1024 * 1024):.2f} MB\n"
    network_info['Bytes Received'] = f"{net_io.bytes_recv / (1024 * 1024):.2f} MB\n"

    # Сетевые интерфейсы
    network_info["Interfaces"] = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # IPv4
                network_info["Interfaces"].append({
                    "Interface": interface,
                    "IP Address": addr.address,
                    "Netmask": addr.netmask,
                })
    return network_info
