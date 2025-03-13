import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor

def ping_ip(ip):
    """Пингует IP-адрес и возвращает его, если он доступен."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "2", ip]  # '2->1'
    try:
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2, check=True)
        return ip
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None

def scan_network(network):
    """Сканирует указанную сеть."""
    ip_list = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(ping_ip, f"{network}.{i}") for i in range(1, 255)]
        for future in futures:
            result = future.result()
            if result:
                ip_list.append(result)
    return ip_list

print("scanner_of_ip")

if __name__ == "__main__":
    subnet = input("Введите подсеть (например, 192.168.1): ")
    print("Сканирование сети, пожалуйста, подождите...")
    available_ips = scan_network(subnet)
    print("Доступные устройства:")
    for ip in available_ips:
        print(ip)


# Этот код выполняет **сканирование локальной сети** для поиска активных устройств с использованием функции пинга. Он подходит для определения доступных IP-адресов в указанной подсети.

# ### Описание функциональности:
# 1. **Функция `ping_ip`**:
#    - Выполняет пинг указанного IP-адреса:
#      - Определяет операционную систему (`Windows` или другие) и выбирает соответствующий параметр пинга (`-n` для Windows, `-c` для Unix-подобных систем).
#      - Запускает команду `ping` через `subprocess.run` с таймаутом 2 секунды.
#      - Если команда успешна, возвращает IP-адрес; иначе — `None`.

# 2. **Функция `scan_network`**:
#    - Принимает подсеть (например, `192.168.1`) и проверяет доступность всех адресов от `.1` до `.254`.
#    - Использует `ThreadPoolExecutor` для многопоточной обработки:
#      - Создает пул потоков с 50 рабочими.
#      - Параллельно вызывает `ping_ip` для всех IP в указанной подсети.
#      - Сохраняет доступные IP-адреса в список.

# 3. **Основной блок**:
#    - Запрашивает подсеть у пользователя.
#    - Вызывает `scan_network` для сканирования.
#    - Выводит список доступных устройств.

# ### Пример работы:
# 1. Пользователь вводит подсеть: `192.168.1`.
# 2. Скрипт проверяет доступность всех IP-адресов от `192.168.1.1` до `192.168.1.254`.
# 3. После завершения сканирования выводит список активных устройств, например:
#    ```
#    Доступные устройства:
#    192.168.1.2
#    192.168.1.10
#    192.168.1.100
#    ```

# ### Особенности:
# - **Многопоточность**: Использование `ThreadPoolExecutor` значительно ускоряет процесс сканирования.
# - **Поддержка разных ОС**: Автоматическое определение параметра пинга в зависимости от системы.

# ### Возможные улучшения:
# 1. **Обработка исключений**:
#    - Добавить обработку ошибок в случае некорректного ввода подсети.
# 2. **Параметры сканирования**:
#    - Возможность задания диапазона IP (например, `.50`-`.100`) для более точного сканирования.
# 3. **Оптимизация вывода**:
#    - Добавить отображение прогресса (например, через библиотеку `tqdm`).
# 4. **Логирование**:
#    - Сохранять результаты в файл для дальнейшего анализа.
# 5. **IPv6**:
#    - Расширить функционал для поддержки адресов IPv6.