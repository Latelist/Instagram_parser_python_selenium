def login_instructions():
    print("Открываю Инстаграм")
    print("Войдите в Инстаграм")
    input("Когда войдёте, нажмите Энтер")

def greeting_message():
    input("Привет! Я помогу спарсить профиль пользователя в Инстаграм. Нажмите Энтер, чтобы я открыл браузер\n")

def show_login_success():
    input("Вы успешно вошли! Нажмите Энтер, чтобы продолжить\n")

def show_login_failure():
    input("Что-то пошло не так. Попробуйте повторить вход и нажмите Энтер\n")

def ask_for_URL():
    URL = input("Введите URL профиля, который хотите спарсить, и нажмите Энтер\n")
    return URL

def quit():
    var = input("Парсинг завершён. Нажмите Энтер, чтобы продолжить, или q, чтобы выйти\n")
    if var == "q":
        return False
    else:
        return True