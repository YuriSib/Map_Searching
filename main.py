from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from bs4 import BeautifulSoup
import pickle


from exchange_with_xl import import_xl, export_xl


def settings():
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = "http://1257421-all-country-DE:1wpldj8s1z@93.190.142.139:13736"
    # proxy.ssl_proxy = "https://your_proxy_server:port"
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
    wait = WebDriverWait(driver, 20)

    element = wait.until(EC.visibility_of_element_located(("xpath", "//span[@class='input__context']/input[@class='input__control _bold']")))
    element.send_keys(qwery)
    ActionChains(driver).send_keys(Keys.RETURN).perform()

    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    price_html = soup.find('span', {'class': 'business-features-view__valued-value'})
    if price_html:
        price = price_html.get_text(strip=True).split()[0]
    else:
        price = "Значение не найдено"

    html_qnt_ratings = soup.find('div', {'class': 'business-rating-with-text-view__count'})
    if html_qnt_ratings:
        qnt_ratings = html_qnt_ratings.get_text(strip=True).split()[0]
    else:
        qnt_ratings = "Значение не найдено"

    try:
        choice = driver.find_element('xpath', '''/html/body/div[1]/div[2]/div[8]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/ul/li[1]/div/div/div''')
        if choice:
            element = choice
        else:
            element = driver.find_element("xpath", '''/html/body/div[1]/div[2]/div[8]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/ul/li[1]/div/div/div/div/div[2]/div[1]''')
        element.click()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        coordinates = driver.current_url.split('=')[1].split('&')[0]
        coordinates_a, coordinates_b = coordinates.split('%2C')[0], coordinates.split('%2C')[1]
        coordinates = f'{coordinates_b}, {coordinates_a}'

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        if "Значение не найдено" in qnt_ratings:
            html_qnt_ratings = soup.find('span', {'class': 'business-rating-amount-view'})
            if html_qnt_ratings:
                qnt_ratings = html_qnt_ratings.get_text(strip=True).split()[0]
            else:
                qnt_ratings = "Значение не найдено"

        working_hours = soup.find_all('div', {'class': 'business-contacts-view__block'})[2].\
            find('div', {'class': 'card-feature-view__content'}).get_text(strip=True)
        if working_hours != 'График работы не указан':
            pass

        rating = soup.find('span', {'class': 'business-rating-badge-view__rating-text _size_m'}).get_text(strip=True)
        if "Рейтинг" in rating:
            rating = rating.strip('Рейтинг')

        html_qnt_feedback = soup.find('div', {'class': 'business-header-rating-view__text _clickable'})
        if html_qnt_feedback.text:
            qnt_feedback = html_qnt_feedback.get_text(strip=True).split()[0]
        else:
            html_qnt_feedback = soup.find('div', {'class': 'business-card-title-view__header'})
            qnt_feedback = html_qnt_feedback.get_text(strip=True).split()[0] if html_qnt_feedback.text else "Значение не найдено"

        type_ = soup.find('a', {'class': 'business-card-title-view__category _outline'}).get_text(strip=True)

        if working_hours != 'График работы не указан' and working_hours != 'Круглосуточно' and working_hours != 'Больше не работает':
            element = driver.find_elements("xpath","//div[@class='business-working-status-view _closed']")
            if element:
                element[0].click()
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                html3 = driver.page_source
                soup3 = BeautifulSoup(html3, 'lxml')
                working_hours = soup3.find('div', {'class': 'business-dialog-view__content'}).get_text(strip=True)
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            html_qnt_ratings = soup.find('div', {'class': 'business-summary-rating-badge-view__rating-count'})
            if html_qnt_ratings:
                qnt_ratings = html_qnt_ratings.get_text(strip=True).split()[0]
            else:
                qnt_ratings = "Значение не найдено"

    except Exception:
        element = driver.find_elements("xpath", '''/html/body/div[1]/div[2]/div[9]/div[1]/div[1]/div[1]/div/div[1]/div/div/div[3]/div[2]/div[2]/h1/a''')
        element[0].click()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        coordinates = driver.current_url.split('=')[1].split('&')[0]
        coordinates_a, coordinates_b = coordinates.split('%2C')[0], coordinates.split('%2C')[1]
        coordinates = f'{coordinates_b}, {coordinates_a}'

        html2 = driver.page_source
        soup2 = BeautifulSoup(html2, 'lxml')

        working_hours = soup2.find('div', {'class': 'orgpage-header-view__working-status'}).get_text(strip=True)
        if working_hours != 'График работы не указан' and working_hours != 'Круглосуточно' and working_hours != 'Больше не работает':
            element = driver.find_elements("xpath","//div[@class='business-working-status-view _closed']")
            if element:
                element[0].click()
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                html3 = driver.page_source
                soup3 = BeautifulSoup(html3, 'lxml')
                working_hours = soup3.find('div', {'class': 'business-dialog-view__content'}).get_text(strip=True)
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

        rating = soup2.find('div', {'class': 'business-rating-badge-view__rating'}).get_text(strip=True)
        if "Рейтинг" in rating:
            rating = rating.strip('Рейтинг')

        qnt_feedback = soup2.find('div', {'class': 'business-header-rating-view__text _clickable'}).get_text(strip=True).split()[0]
        type_ = soup2.find_all('a', {'class': 'breadcrumbs-view__breadcrumb _outline'})[2].get_text(strip=True)

        if "Значение не найдено" in qnt_ratings:
            element = driver.find_elements("xpath", '''//div[@class='carousel__item _align_center']/div[@class='tabs-select-view__title _name_reviews']''')
            if element:
                element[0].click()

            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            html2 = driver.page_source
            soup2 = BeautifulSoup(html2, 'lxml')
            html_qnt_ratings = soup2.find('div', {'class': 'business-summary-rating-badge-view__rating-count'})
        if html_qnt_ratings:
            qnt_ratings = html_qnt_ratings.get_text(strip=True).split()[0]
        else:
            qnt_ratings = "Значение не найдено"

    driver.close()
    driver.quit()

    return coordinates, type_, working_hours, rating, qnt_ratings, qnt_feedback, price


def main():
    with open('data.pickle', 'rb') as file:
        qwery_list = pickle.load(file)
        row = 8
    for qwery in qwery_list[6:]:
        try:
            if 'лица' not in qwery:
                coordinates, type_, working_hours, rating, qnt_ratings, qnt_feedback, price = scrapper(qwery)
            else:
                print('Нельзя искать улицы')
                raise Exception
        except Exception as e:
            print(e)
            coordinates, type_, working_hours, rating, qnt_ratings, qnt_feedback, price = '0', '0', '0', '0', '0', '0', '0'

        export_xl(coordinates, type_, working_hours, rating, qnt_ratings, qnt_feedback, price, row)
        print(row)
        row += 1


if __name__ == '__main__':
    main()








