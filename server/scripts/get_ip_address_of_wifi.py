import psutil
import socket


def get_ip_address_of_wifi():
    interfaces = psutil.net_if_addrs()
    for interface, addresses in interfaces.items():
        # Проверяем, относится ли интерфейс к Wi-Fi (обычно это что-то вроде 'Wi-Fi', 'wlan0', и т.д.)
        if 'Wi-Fi' in interface or 'wlan' in interface or 'Wireless' in interface or 'wlan0' in interface or 'eth0' in interface:
            for address in addresses:
                if address.family == socket.AF_INET:  # IPv4 адрес
                    return address.address

    return "Не удалось найти Wi-Fi интерфейс."


print("get_ip_address_of_wifi -> " + get_ip_address_of_wifi())
address = get_ip_address_of_wifi()
