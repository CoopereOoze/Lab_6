import os
import re
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

ROOT = Path(__file__).parent.resolve()


def pytest_addoption(parser):
    parser.addoption('--base-url', default='https://ya.ru')
    parser.addoption('--headed', action='store_true')


@pytest.fixture
def base_url(request):
    return request.config.getoption('--base-url')


@pytest.fixture
def browser(request):
    options = Options()
    options.page_load_strategy = 'eager'
    if not request.config.getoption('--headed'):
        options.add_argument('--headless=new')
    options.add_argument('--window-size=1440,1000')
    if os.getenv('CHROME_BINARY'):
        options.binary_location = os.environ['CHROME_BINARY']
    # Явный путь удобен для воспроизводимого прогона и параллельных worker.
    executable = os.getenv('CHROMEDRIVER')
    if not executable:
        executable = ChromeDriverManager(
            cache_manager=DriverCacheManager(root_dir=str(ROOT / '.driver-cache'))
        ).install()
    driver = webdriver.Chrome(service=Service(executable), options=options)
    driver.implicitly_wait(0)
    driver.set_page_load_timeout(30)
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    driver = item.funcargs.get('browser')
    if report.when == 'call' and driver is not None:
        # Изображение фиксирует реальный браузер и сохраняется для любого исхода.
        worker = os.getenv('PYTEST_XDIST_WORKER', 'main')
        name = re.sub(r'[^A-Za-z0-9_-]+', '_', item.name)[:120]
        folder = ROOT / 'screenshots'
        folder.mkdir(exist_ok=True)
        path = folder / f'{worker}_{name}.png'
        driver.save_screenshot(str(path))
        allure.attach.file(str(path), name='Состояние браузера',
                           attachment_type=allure.attachment_type.PNG)
        allure.attach(driver.current_url, name='URL',
                      attachment_type=allure.attachment_type.TEXT)
        if report.failed:
            allure.attach(driver.page_source, name='HTML',
                          attachment_type=allure.attachment_type.HTML)

