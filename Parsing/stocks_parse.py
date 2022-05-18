import logging
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from Data.data import chromeDriver_path
from utils.db_api.db_work import update_USA_stocks_table, update_Russia_stocks_table


def _update_russia_stocks_page():
    browser_options = webdriver.ChromeOptions()
    userAgent = UserAgent()
    browser_options.add_argument(f"user-agent={userAgent.random}")
    browser_options.headless = False
    driver = webdriver.Chrome(
        executable_path=chromeDriver_path,
        options=browser_options
    )
    try:
        driver.get(f'https://ru.tradingview.com/markets/stocks-russia/market-movers-all-stocks/')
        time.sleep(3)
        # cookie_accept_btn = driver.find_element_by_class_name('content-YKkCvwjV')
        # cookie_accept_btn.click()
        while True:
            try:
                load_more_btn = driver.find_element_by_class_name('loadButton-59hnCnPW')
                load_more_btn.click()
                time.sleep(3)
            except Exception:
                break
    except Exception:
        pass
    finally:
        with open(fr'C:\Users\Макс\PycharmProjects\tgbot\Parsing\WebPagesCopies\all_russia_stocks.html', 'w',
                  encoding='utf-8') as file:
            file.write(driver.page_source)
        driver.close()
        driver.quit()


def russia_stocks_parse():
    week_day = datetime.today().weekday()
    while True:
        if week_day < 5:
            start_time = datetime.now()
            _update_russia_stocks_page()
            with open(fr'C:\Users\Макс\PycharmProjects\tgbot\Parsing\WebPagesCopies\all_russia_stocks.html', 'r',
                      encoding='utf-8') as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            stocks_table = soup.find_all(class_='tableWrap-zFfoQ8VE')[0]
            parse_data = []
            for stock in stocks_table:
                data = stock.find_all('td')
                result = [data[i].text.strip() for i in range(6)]
                result[0] = stock.find('sup', class_='apply-common-tooltip tickerDescription-qN79lDF8').text.strip()
                result.append(stock.find('a', class_='apply-common-tooltip tickerName-qN79lDF8').text.strip())
                parse_data.append(result)
            for line in parse_data:
                update_Russia_stocks_table(line)
                # start_russia(line)
            logging.info('SUCCESSFUL russia STOCKS TABLE UPDATE')
            logging.info(f'russia stocks parse time: {datetime.now() - start_time}')
            time.sleep(5)
        else:
            time.sleep(10)


def usa_stocks_parse():
    week_day = datetime.today().weekday()
    while True:
        if week_day != 0:
            try:
                pages = {'most-active': 300, 'gainers': 100, 'losers': 1100}
                start_time = datetime.now()
                userAgent = UserAgent()
                headers = {'user-agent': userAgent.random}
                result = []
                for page_name, iter_count in pages.items():
                    for i in range(0, iter_count, 100):
                        url = f'https://finance.yahoo.com/{page_name}?offset={i}&count=100'
                        req = requests.get(url, headers=headers)
                        src = req.text
                        soup = BeautifulSoup(src, 'lxml')
                        table = soup.find('table', class_='W(100%)')
                        body = table.find('tbody').find_all('tr')
                        for element in body:
                            tds = element.find_all('td')
                            lst = [td.text.strip() for td in tds]
                            result.append(lst)
                result = [tuple(x) for x in result]
                result = list(set(result))
                result.sort(key=lambda x: (x[0]))
                for line in result:
                    # start_usa(line)
                    update_USA_stocks_table(data=line)

                logging.info('SUCCESSFUL USA STOCKS PARSE')
                logging.info(f'USA STOCKS PARSE TIME = {datetime.now() - start_time}')
            except Exception as ex:
                continue
        else:
            time.sleep(10)
