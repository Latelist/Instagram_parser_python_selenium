from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


from dotenv import load_dotenv
import os

def start_driver():
    service = Service("/Users/salatzelenyj/Desktop/Chromedriver/chromedriver")
    driver = webdriver.Chrome(service=service)
    return(driver)

def load_login_data():
    load_dotenv()
    IG_username = os.getenv("IG_USERNAME")
    IG_password = os.getenv("IG_PASSWORD")

    if IG_username is None or IG_password is None:
        raise ValueError("Логин и пароль не загрузились из окружения")

    return IG_username, IG_password

def open_inst(driver):
    driver.get("https://www.instagram.com/")

def login_auto(driver, IG_username, IG_password):
    driver.get("https://www.instagram.com/accounts/login/")

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(IG_username)
    password_input.send_keys(IG_password)
    password_input.send_keys(Keys.RETURN)

def login_manually(driver):
    driver.get("https://www.instagram.com/accounts/login/")

def is_logged_in(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'Фото профиля')]"))
        )
        return True
    except Exception as e:
        return False

def open_profile(driver, URL):
    try:
        driver.get(URL)
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//header//ul//li")))
    except Exception as e:
        print("Ошибка. Кажется, сессия закрылась.")
        print("Подробности: ", e)

def get_username(driver):
    try:
        username_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//header//h2/span"))
            )
        print("Имя пользователя: ", username_element.text)
    except Exception as e:
        print("Не нашёл, сорян")

