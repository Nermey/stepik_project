import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fastapi import APIRouter


def setup_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--disable-webrtc")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def get_course(driver: webdriver.Chrome, query: str) -> tuple:
    url = f"https://stepik.org/catalog/search?free=true&q={query}"
    driver.get(url)

    time.sleep(10)

    # Парсинг страницы
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    # Извлечение курсов
    courses = soup.find_all("a", class_="course-card__title")
    for course in courses:
        course_name = course.text.strip()

        # Разбиваем текст на слова и ищем точное совпадение
        words = course_name.lower().split()
        if query.lower() in words:
            return course.get("href"), course_name
    return None, None


router = APIRouter(prefix="/courses", tags=["Get Courses by params"])


@router.get("/")
def get_courses(query: str):
    with setup_driver() as driver:
        link, name = get_course(driver, query)
        if link and name:
            return {"link": "https://stepik.org" + link, "name": name}
    return {"error": "No courses found for the given query"}
