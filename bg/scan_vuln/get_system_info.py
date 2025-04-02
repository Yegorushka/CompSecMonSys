import platform
import socket
import psutil

def get_system_info():
    info = {
        "OS": f"{platform.system()}\n",
        "OS Version": f"{platform.version()}\n",
        "OS Release": f"{platform.release()}\n",
        "Architecture": f"{platform.architecture()}\n",
        "Processor": f"{platform.processor()}\n",
        "Hostname": f"{socket.gethostname()}\n",
        "IP Address": f"{socket.gethostbyname(socket.gethostname())}\n",
        "RAM": f"{round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2)} GB\n",
        "CPU Cores": f"{psutil.cpu_count(logical=True)}\n",
        "CPU Usage": f"{psutil.cpu_percent(interval=1)}%\n"
    }
    if psutil.sensors_battery():
        battery = psutil.sensors_battery()
        info["Battery"] = f"{battery.percent}% (Plugged In: {battery.power_plugged})\n"
    else:
        info["Battery"] = "No battery detected\n"
    return info

# print(get_system_info)
