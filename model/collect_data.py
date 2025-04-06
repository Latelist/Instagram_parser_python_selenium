from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re

def get_profile_data(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//header"))
            )
        name = driver.find_element(By.XPATH, "//header//h2/span").text
        posts = driver.find_element(By.XPATH, "//header//ul/li[1]//span//span").text
        followers = driver.find_element(By.XPATH, "//header//ul/li[2]//span//span").text

        data = {
            "name": name,
            "posts": posts,
            "followers": followers
            }

        return data
    except:
        print("Не получилось распознать данные профиля.")
        data = {
            "name": "Noname",
            "posts": "No post info",
            "followers": "No followers info"
        }

def get_post_links(driver): #собирает ссылки на посты, которые уже прогрузились в DOM
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

    post_links = set()
    links = driver.find_elements(By.TAG_NAME, "a") #находит все ссылки в DOM

    for link in links: #фильтрует ссылки и добавляет в результат только ссылки на публикации
        href = link.get_attribute("href")
        if href and "/p/" in href:
            post_links.add(href)
    
    return post_links

def scroll(driver):
    driver.execute_script("window.scrollBy(0, 100);")
    time.sleep(0.5)

def get_all_posts(driver):

    all_posts_links = set()
    scroll_counts = 0
    height_check_counts = 0
    height = driver.execute_script("return document.body.scrollHeight")

    while scroll_counts < 100:
        post_links_pack = get_post_links(driver)
        all_posts_links.update(post_links_pack)
        scroll(driver)
        scroll_counts += 1
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == height:
            height_check_counts += 1
        else:
            height_check_counts = 0
            
        if height_check_counts > 10:
            break
        print("Собираю ссылки на посты. Уже нашёл " + str(len(all_posts_links)))


    return all_posts_links

def extract_number(text):
    clean_text = text.replace('\xa0', '').replace(' ', '')
    match = re.search(r'\d+', clean_text)
    if match:
        return int(match.group())
    else:
        return 0
    
def get_description(driver):
    try: 
        description = " " + driver.find_element(By.XPATH, "//ul//h1").text
    except:
        description = "___________"
    return description

def get_likes(driver):
    try: 
        likes = driver.find_element(By.XPATH, "//section//a//span/span").text
        if len(likes) < 1:
            likes_text = driver.find_element(By.XPATH, "//section//a//span[contains(text(), 'ещё')]/span").text
            number = extract_number(likes_text)
            likes = number + 1
            likes = str(likes)
    except:
        likes = "___________"
    return likes

def get_comments(driver):
    try: 
        comments = len(driver.find_elements(By.XPATH, "//article//ul//li//h3"))
    except:
        comments = "___________"
    return comments

def get_publication_date(driver):
    try: 
        publication_date = driver.find_element(By.XPATH, "//time").get_attribute("datetime")
    except:
        publication_date = "___________"
    return publication_date


def get_post_info(driver, URL):
    driver.get(URL)
    try:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//ul")))
        description = get_description(driver)
        likes = get_likes(driver)
        comments = get_comments(driver)
        publication_date = get_publication_date(driver)

        data = {
            "URl": URL,
            "description": description,
            "likes": likes,
            "comments": comments,
            "publication_date": publication_date          
        }
        return data 
    except:
        print("Не получилось спарсить данные поста: " + URL)
