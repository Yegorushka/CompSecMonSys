import netifaces

gws = netifaces.gateways()
ip_router = list(gws['default'].items())[0][1][0]
print("router_ip -> " + ip_router)
