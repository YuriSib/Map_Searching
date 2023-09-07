from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup

from exchange_with_xl import import_xl


def settings():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    return driver


def scrapper(qwery):
    driver = settings()
    driver.get(url='https://yandex.ru/maps/')
    wait = WebDriverWait(driver, 10)

    driver.find_element("xpath", "//span[@class='input__context']/input[@class='input__control _bold']").send_keys(qwery)
    ActionChains(driver).send_keys(Keys.RETURN).perform()

    element = wait.until(EC.visibility_of_element_located(("xpath",
                                                           '''//div[@class="search-business-snippet-view__title"]''')))
    element.click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    working_hours = soup.find('div', {'class': 'business-card-working-status-view__text'}).get_text(strip=True)
    rating = soup.find('span', {'class': 'business-rating-badge-view__rating-text _size_m'}).get_text(strip=True)
    qnt_ratings = soup.find('div', {'class': 'business-rating-with-text-view__count'}).get_text(strip=True).split()[0]
    qnt_feedback = soup.find('div', {'class': 'business-header-rating-view__text _clickable'}).get_text(strip=True).split()[0]

    driver.quit()

    return working_hours, rating, qnt_ratings, qnt_feedback


def main():
    qwery_list = import_xl(8, 6)
    for qwery in qwery_list:
        scrapper(qwery)


if __name__ == "__main__":
    main()
