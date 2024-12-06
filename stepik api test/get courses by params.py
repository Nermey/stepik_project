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

# Открываем страницу
url = "https://stepik.org/catalog/search?free=true&q=Python"
driver.get(url)

# Ждем появления элемента с заголовком курса
try:
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.CLASS_NAME, "course-card__title"))
    )
    html = driver.page_source
finally:
    # Закрываем браузер
    driver.quit()

# Парсинг с BeautifulSoup
soup = BeautifulSoup(html, "lxml")

# Извлечение курсов
courses = soup.find_all("a", class_="course-card__title")  # Класс заголовка курса

if courses:
    for course in courses:
        link = course.get("href")
        name = course.text.strip()
        print(link, name)
else:
    print("Курсы не найдены.")
