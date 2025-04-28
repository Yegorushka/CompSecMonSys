import psutil
import socket


def get_active_wifi_ip():
    wifi_keywords = ['Wi-Fi', 'wlan', 'Wireless', 'wlan0', 'wlp', 'en0']
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for interface, addresses in interfaces.items():
        # Проверяем: имя похоже на Wi-Fi и интерфейс активен
        if any(keyword in interface for keyword in wifi_keywords) and stats[interface].isup:
            for address in addresses:
                if address.family == socket.AF_INET:
                    return address.address
    return False
