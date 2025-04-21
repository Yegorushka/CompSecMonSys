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
