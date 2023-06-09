import os
import getpass
import re
from datetime import datetime


def create_log_directory():
    # Перевірка на існування директорії перед її створенням
    if not os.path.exists('log_directory'):
        # Створення розділу на диску для системного журналу
        os.mkdir('log_directory')
        # Встановлення прав доступу тільки для адміністратора
        os.chmod('log_directory', 0o700)
    else:
        pass


def check_password_requirements(password):
    # Повертає True, якщо пароль відповідає вимогам, інакше False
    if len(password) == 4:
        return True
    return False


def check_existing_username(username):
    # Перевірка на існування користувача з використанням системного журналу та регулярних виразів
    log_file_path = 'log_directory/user_log.txt'
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            for line in log_file:
                match = re.search(r'Username:\s+(\w+)', line)
                if match and match.group(1) == username:
                    return True
    return False


def save_user_data(username, password):
    # Збереження даних користувача у системному журналі реєстрації
    now = datetime.now()
    registration_time = now.strftime("%Y-%m-%d %H:%M:%S")
    log_file_path = 'log_directory/user_log.txt'
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"Username: {username}, Password: {password}, Registration Time: {registration_time}\n")


def calculate_time_since_registration(registration_time):
    # Визначення, скільки часу пройшло з моменту реєстрації
    now = datetime.now()
    registration_datetime = datetime.strptime(registration_time, "%Y-%m-%d %H:%M:%S")
    time_elapsed = now - registration_datetime
    return time_elapsed


def register_user():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    # Перевірка за допомогою регулярного виразу наявності користувача
    if check_existing_username(username):
        print("Username already exists. Please choose a different username.")
        return

    if check_password_requirements(password):
        save_user_data(username, password)
        print("User registered successfully!")
    else:
        print("Password does not meet the requirements.")


def main():
    create_log_directory()
    register_user()


if __name__ == '__main__':
    main()
