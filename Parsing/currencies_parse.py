from datetime import datetime
import logging
import time
from selenium import webdriver
from Data.data import chromeDriver_path
from bs4 import BeautifulSoup
from utils.db_api.db_work import update_currencies_table
from fake_useragent import UserAgent


def _update_all_currencies_page():
    browser_options = webdriver.ChromeOptions()
    userAgent = UserAgent()
    browser_options.add_argument(f"user-agent={userAgent.random}")
    browser_options.headless = False
    driver = webdriver.Chrome(
        executable_path=chromeDriver_path,
        options=browser_options
    )
    try:
        driver.get('https://ru.tradingview.com/markets/currencies/rates-all/')
        time.sleep(3)
        # cookie_accept_btn = driver.find_element_by_class_name('content-YKkCvwjV')
        # cookie_accept_btn.click()
        while True:
            try:
                load_more_btn = driver.find_element_by_class_name('tv-load-more__btn')
                load_more_btn.click()
                time.sleep(3)
            except Exception:
                break
    except Exception:
        pass
    finally:
        with open(r'C:\Users\Макс\PycharmProjects\tgbot\Parsing\WebPagesCopies\all_currencies.html', 'w',
                  encoding='utf-8') as file:
            file.write(driver.page_source)
        driver.close()
        driver.quit()


def parse_all_currencies():
    week_day = datetime.today().weekday()
    while True:
        if week_day < 5:
            start_time = datetime.now()
            _update_all_currencies_page()
            with open(r'C:\Users\Макс\PycharmProjects\tgbot\Parsing\WebPagesCopies\all_currencies.html', 'r',
                      encoding='utf-8') as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            currencies_table = soup.find_all(class_='tv-data-table__tbody')[1]
            for currency in currencies_table:
                data = currency.find_all('td')
                result = [data[i].text.strip() for i in range(9)]
                update_currencies_table(result)
                # start_currencies(result)
            logging.info('SUCCESSFUL CURRENCIES TABLE UPDATE')
            logging.info(f'currencies parse time: {datetime.now() - start_time}')
            time.sleep(5)
        else:
            time.sleep(10)
