from aiogram import Dispatcher, executor

from utils.monitoring import subscribes_monitoring
from utils.set_bot_commands import set_default_commands
from Handlers import *
from Handlers.first_choice import *
from Parsing.currencies_parse import parse_all_currencies
from Parsing.stocks_parse import usa_stocks_parse, russia_stocks_parse
import threading
from variables import bot
from utils.users_work import load_users


async def on_shutdown(dispatcher: Dispatcher):
    await bot.close()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


async def start_working(dispatcher: Dispatcher):
    await set_default_commands(dispatcher)
    load_users()
    threading.Thread(target=parse_all_currencies).start()
    threading.Thread(target=russia_stocks_parse).start()
    threading.Thread(target=usa_stocks_parse).start()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_working, on_shutdown=on_shutdown)
