from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


def get_course(query: str) -> tuple:
    # Открываем страницу
    url = f"https://stepik.org/catalog/search?free=true&q={query}"
    driver.get(url)

    # Ждем появления элемента с заголовком курса
    try:
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "course-card__title"))
        )
        html = driver.page_source
    finally:
        driver.quit()

    # Парсинг с BeautifulSoup
    soup = BeautifulSoup(html, "lxml")

    # Извлечение курсов
    courses = soup.find("a", class_="course-card__title")  # Класс заголовка курса

    return courses.get("href"), courses.text.strip() if courses else None


print(get_course("sql"))
print(get_course("python"))
print(get_course("git"))
print(get_course("fast api"))
print(get_course("ООП"))
