import getpass
import re
import time

error_count = {}
delta_t = 180
log_file_path = 'log_directory/user_log.txt'


def authenticate(username, password):
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            match = re.search(r'Username:\s+(\w+), Password:\s+(\w+)', line)
            if match and match.group(1) == username and match.group(2) == password:
                return True
    return False


def secret_function_authentication():
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            match = re.search(r'Value:\s+(\w+)', line)
            x = float(input("Enter x: "))
            if match:
                result = float(match.group(1)) * x + 1.5
                user_result = float(input("Enter result of a * x + 1.5 = "))
                if result == user_result:
                    return True
    return False


def ask_questions():
    questions = ["Your favourite number?", "Your favourite colour?", "Your favourite alcohol?"]
    answers = []

    for question in questions:
        answer = input(question + " ")
        answers.append(answer)

    number, colour, alcohol = answers

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            match = re.search(r'Number:\s+(\w+), Colour:\s+(\w+), Alcohol:\s+(\w+)', line)
            if match and match.group(1) == number and match.group(2) == colour and match.group(3) == alcohol:
                return True

    return False


def main():
    while True:
        username = input("Enter your username: ")
        password = getpass.getpass("Enter password: ")
        if authenticate(username, password):
            if ask_questions():
                if secret_function_authentication():
                    print("Authentication successful!")
                    break
                else:
                    print("Authentication failed. Please try again.")
                    time.sleep(delta_t)
            else:
                print("Authentication failed. Please try again.")
                time.sleep(delta_t)
        else:
            print("Authentication failed. Please try again.")
        error_count[username] = error_count.get(username, 0) + 1
        if error_count[username] == 5:
            print("Maximum number of errors reached. Please contact the administrator for registration.")
            break


if __name__ == "__main__":
    main()
