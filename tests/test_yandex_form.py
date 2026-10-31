import allure
import pytest

from pages.yandex_form_page import YandexFormPage


@pytest.mark.ui
@allure.suite('Форма поиска Яндекс')
class TestYandexSearch:
    @allure.title('Поиск по запросу {query}')
    @pytest.mark.parametrize('query,expected', [
        ('Selenium WebDriver', 'selenium'),
        ('Python автоматизация тестирования', 'python'),
        ('Тестирование программного обеспечения', 'тестирован'),
    ])
    def test_search(self, browser, base_url, query, expected):
        page = YandexFormPage(browser).open(base_url).enter(query).submit()
        with allure.step('Проверить запрос и первый результат'):
            assert page.submitted_query() == query
            title = page.first_result_text().strip()
            assert title, 'Заголовок первого результата пуст'
            assert expected in title.casefold(), title

    @allure.title('Подсказки при вводе запроса')
    def test_suggest(self, browser, base_url):
        (YandexFormPage(browser).open(base_url)
         .enter('автоматизация тестирования').wait_for_suggestions())

    @allure.title('Очистка поисковой строки')
    def test_clear(self, browser, base_url):
        page = YandexFormPage(browser).open(base_url).enter('текст для очистки')
        assert page.value() == 'текст для очистки'
        assert page.clear().value() == ''

    @allure.title('Отправка запроса клавишей Enter')
    def test_enter(self, browser, base_url):
        query = 'Selenium WebDriver'
        page = YandexFormPage(browser).open(base_url).enter(query).submit('enter')
        assert page.submitted_query() == query
        assert page.first_result_text().strip()

