# Лабораторная работа 6

Тесты формы поиска https://ya.ru. Нужны Python 3.12, Google Chrome и Node.js.

## Запуск

Откройте PowerShell в этой папке:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm install
.\.venv\Scripts\python.exe -m pytest -v --alluredir=results-new/sequential
.\.venv\Scripts\python.exe -m pytest -n 2 -v --alluredir=results-new/parallel
```

Для запуска двух проверок, которые прошли параллельно в отчете:

```powershell
.\.venv\Scripts\python.exe -m pytest -n 2 -v -k "suggest or clear" --alluredir=results-new/form
```

Драйвер загружается автоматически. Для параллельного запуска можно заранее задать путь к совместимому ChromeDriver:

```powershell
$env:CHROMEDRIVER = 'C:\путь\к\chromedriver.exe'
```

Флаг `--headed` показывает окно браузера. Переменная `CHROME_BINARY` задает путь к Chrome, если он установлен нестандартно.

## Allure

Готовые отчеты открываются прямо в браузере: `reports/sequential.html` и `reports/parallel.html`.

Создать отчет после нового запуска:

```powershell
npx allure generate results-new/sequential --output reports-new/sequential
npx allure open reports-new/sequential
```

Повторно собрать отчет из приложенных исходных результатов:

```powershell
npx allure generate allure-results/sequential --output reports-new/saved
```

## Файлы по шагам задания

| Шаг | Файлы |
|---|---|
| 1. Окружение | requirements.txt, package.json |
| 2. Базовая конфигурация | conftest.py |
| 3. Page Object | pages/yandex_form_page.py |
| 4. Тесты | tests/test_yandex_form.py |
| 5. Параллельный запуск | pytest.ini, logs/parallel.txt |
| 6. Allure | allure-results/, reports/, screenshots/ |
| 7. Документация | README.md |

## Сохраненные результаты

Полный запуск — 2 passed, 4 broken из-за CAPTCHA; повторный запуск подсказок и очистки в двух процессах — 2 passed. Полный запуск был выполнен до смены стратегии загрузки на eager; параллельный — после. Исходные JSON, вложения, логи и скриншоты сохранены отдельно от будущих запусков.
