import psutil

def get_active_connections():
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED':
            connections.append({
                "Local Address": f"{conn.laddr.ip}:{conn.laddr.port}\n",
                "Remote Address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A\n",
                "Status": conn.status
            })
    return connections