import asyncio

from utils.db_api.db_work import get_stock_price
from variables import bot
import sqlite3
from utils.users_work import subscribes_price_delete


async def subscribes_monitoring(user_id: int):
    from utils.users_work import get_subscribes_and_prices
    while True:
        with sqlite3.connect('investments.db', check_same_thread=True) as conn:
            cursor = conn.cursor()
            values = get_subscribes_and_prices(user_id)
            if values == {}:
                await asyncio.sleep(5)
                continue
            for ticker, prices in values.items():
                current_price = get_stock_price(ticker)
                if current_price is None:
                    current_price = cursor.execute(f"""SELECT last_price FROM RussiaStocksTable
                        WHERE ticker = {ticker}""").fetchone()
                for price in prices:
                    if float(price[0]) <= float(price[1]) <= float(current_price) \
                            or float(price[0]) >= float(price[1]) >= float(current_price):
                        # Отправляем сообщение пользователю
                        await bot.send_message(user_id, text=f"{ticker} достиг цены {price[1]}!")
                        subscribes_price_delete(user_id, ticker, price[1])
            await asyncio.sleep(5)
