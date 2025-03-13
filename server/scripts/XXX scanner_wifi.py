import scapy.all as sc

def scan_network(network):
    arp_request = sc.ARP(pdst=network)
    broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = sc.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices = []
    for sent, received in answered_list:
        devices.append({"IP": received.psrc, "MAC": received.hwsrc})

    return devices

# Укажи свою сеть (например, 192.168.1.1/24)
network = "192.168.2.1/24"  
devices = scan_network(network)

print("Найденные устройства в сети:")
for device in devices:
    print(f"IP: {device['IP']} - MAC: {device['MAC']}")
