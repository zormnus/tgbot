import json
import logging

from Exceptions.exceptions import IncorrectTicker

__data = {}


def load_users():
    global __data
    with open('users.json', 'r') as file:
        __data = json.load(file)


def write(data: str):
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=True)


def check_user(user_id: int, username: str):
    if str(user_id) not in json.dumps(__data):
        __data['users']['count'] += 1
        new_user_data = {'name': username, 'id': int(user_id), 'events': {}}
        __data['users']['items'].append(new_user_data)
        write(__data)
        logging.info(f'USER {user_id} has been created')
    else:
        logging.info(f'USER {user_id} already exists')


def add_ticker(user_id: str, ticker: str):
    ticker = ticker.upper().strip()
    result = list(filter(lambda item: item['id'] == user_id, __data['users']['items']))
    tickers = list(result[0]['events'].keys())
    if ticker not in tickers:
        tickers_index = __data['users']['items'].index(result[0])
        res = __data['users']['items'][tickers_index]['events']
        res[ticker] = []
        __data['users']['items'][tickers_index]['events'] = res
        write(__data)
    else:
        raise IncorrectTicker(text=f'Вы уже отслеживаете котировки компании {ticker}')


def delete_ticker(user_id: str, ticker: str) -> int:
    ticker = ticker.upper().strip()
    result = list(filter(lambda item: item['id'] == user_id, __data['users']['items']))
    tickers = list(result[0]['events'].keys())
    if ticker in tickers:
        tickers_index = __data['users']['items'].index(result[0])
        res = __data['users']['items'][tickers_index]['events']
        del res[ticker]
        __data['users']['items'][tickers_index]['events'] = res
        write(__data)
    else:
        raise IncorrectTicker(text=f'Вы не отслеживаете котировки {ticker}, поэтому я не могу '
                                   'удалить этот тикер из вашего списка')


def get_subscribes_tickers(user_id: str) -> list:
    result = list(filter(lambda item: item['id'] == user_id, __data['users']['items']))
    return list(result[0]['events'].keys())


def get_subscribes_and_prices(user_id: str) -> dict:
    result = list(filter(lambda item: item['id'] == user_id, __data['users']['items']))
    tickers_and_prices = dict(result[0]['events'])
    s = {}
    for ticker, prices in tickers_and_prices.items():
        if prices:
            s[ticker] = prices
    return s


def subscribe_price_add(user_id: int, ticker: str, price: float) -> int:
    from utils.db_api.db_work import get_stock_price
    try:
        result = list(filter(lambda item: item['id'] == user_id, __data['users']['items']))[0]
        user_index = __data['users']['items'].index(result)
        events = result['events']
    except IndexError as ie:
        raise IncorrectTicker('e')
    if ticker not in events.keys():
        raise IncorrectTicker('Вы не отслеживаете котировки этой компании'
                              '\nСперва добавьте её в ваш список с помощью /addstock')
    new_price = [get_stock_price(ticker), price]
    events[ticker].append(new_price)
    __data['users']['items'][user_index]['events'] = events
    write(__data)


def _get_index(data: list, price: float) -> int:
    for i in range(len(data)):
        if data[i][1] == price:
            return i
    return -1


def subscribes_price_delete(user_id: int, ticker: str, price: float):
    try:
        result = list(filter(lambda item: item['id'] == user_id, __data['users']['items']))[0]
        user_index = __data['users']['items'].index(result)
        events = result['events']
    except IndexError as e:
        return
    price_index = _get_index(events[ticker], price)
    try:
        del events[ticker][price_index]
    except ValueError as e:
        return
    finally:
        __data['users']['items'][user_index]['events'] = events
        write(__data)
