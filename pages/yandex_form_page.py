from urllib.parse import parse_qs, urlparse

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class YandexFormPage:
    """Page Object формы поиска; сайт остается внешней зависимостью."""

    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[name="text"],textarea[name="text"]')
    SEARCH_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    SUGGESTIONS = (By.CSS_SELECTOR, '.mini-suggest__popup-content,.mini-suggest__popup')
    RESULTS = (By.CSS_SELECTOR, '#search-result .serp-item')
    RESULT_LINKS = (By.CSS_SELECTOR, '#search-result .serp-item h2 a')

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def guard_captcha(self):
        text = self.driver.find_element(By.TAG_NAME, 'body').text.casefold()
        if 'showcaptcha' in self.driver.current_url or 'подтвердите, что вы не робот' in text:
            raise RuntimeError('Доступ к Яндекс ограничен CAPTCHA; обход не выполняется')

    @allure.step('Открыть форму поиска')
    def open(self, url):
        self.driver.get(url)
        self.guard_captcha()
        self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        return self

    @allure.step('Ввести запрос {text}')
    def enter(self, text):
        field = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        field.clear()
        field.send_keys(text)
        return self

    @allure.step('Очистить поисковую строку')
    def clear(self):
        self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT)).clear()
        return self

    def value(self):
        return self.driver.find_element(*self.SEARCH_INPUT).get_attribute('value')

    @allure.step('Дождаться поисковых подсказок')
    def wait_for_suggestions(self):
        self.wait.until(EC.visibility_of_element_located(self.SUGGESTIONS))
        return self

    @allure.step('Отправить поисковый запрос')
    def submit(self, method='button'):
        if method == 'enter':
            self.driver.find_element(*self.SEARCH_INPUT).send_keys(Keys.ENTER)
        else:
            self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON)).click()
        self.wait.until(lambda d: '/search' in d.current_url or 'showcaptcha' in d.current_url)
        self.guard_captcha()
        self.wait.until(EC.visibility_of_element_located(self.RESULTS))
        return self

    def submitted_query(self):
        return parse_qs(urlparse(self.driver.current_url).query).get('text', [''])[0]

    def first_result_text(self):
        return self.wait.until(EC.visibility_of_element_located(self.RESULT_LINKS)).text

