from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from Data import data
import logging
import asyncio

from Exceptions.exceptions import IncorrectTicker
from utils.db_api.db_work import get_all_stocks_tickers, get_all_currencies_tickers


# Функция проверяющая существование валютных и акционных тикеров в БД
def check_ticker(ticker: str, currencies=True):
    if len(ticker.split()) != 1:
        raise IncorrectTicker('Введён некорректный тикер')
    if currencies:
        if ticker not in existing_currencies_tickers:
            raise IncorrectTicker('Введён несуществующий тикер')
        return
    if ticker not in existing_stocks_tickers:
        raise IncorrectTicker(text='Введён несуществующий тикер')


storage = MemoryStorage()
loop = asyncio.get_event_loop()
bot = Bot(token=data.API_TOKEN)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.DEBUG)
existing_stocks_tickers = sorted(list(set(get_all_stocks_tickers())))
existing_currencies_tickers = sorted(list(set(get_all_currencies_tickers())))
