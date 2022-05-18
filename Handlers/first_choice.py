from aiogram.types import Message

from variables import dp
from aiogram.dispatcher.filters import Text
from Handlers.get_currencies import currencies_register
from Keyboards.markups import stocksMenu, mainMenu, subscribesMenu
from variables import bot
from Handlers.stocks_work import addstock_register, deletestock_register, showstocks_register
from Handlers.subscribes_work import subscribe_add, subscribe_delete, getSubscribes


@dp.message_handler(Text('Акции📊'))
async def stocks_first(msg: Message):
    await bot.send_message(msg.from_user.id, text='Отлично!\nЧто конкретно вас интересует?', reply_markup=stocksMenu)


@dp.message_handler(Text('В главное меню◀️'))
async def to_main_menu(msg: Message):
    await msg.answer(text='Перехожу в главное меню', reply_markup=mainMenu)


@dp.message_handler(Text('Добавить акцию в ваш список'))
async def add_stock(msg: Message):
    await addstock_register(msg)


@dp.message_handler(Text('Удалить акцию из вашего списка'))
async def add_stock(msg: Message):
    await deletestock_register(msg)


@dp.message_handler(Text('Показать текущую информацию по вашим акциям'))
async def add_stock(msg: Message):
    await showstocks_register(msg)


@dp.message_handler(Text('Валюты💵'))
async def currencies_first(msg: Message):
    await currencies_register(msg)


@dp.message_handler(Text('Уведомить о достижении цены'))
async def subscribes_first(msg: Message):
    await msg.reply(text='Добавить новую цену или удалить старую?', reply=False, reply_markup=subscribesMenu)


@dp.message_handler(Text('➕'))
async def subscribe_add_byBtn(msg: Message):
    await subscribe_add(msg)


@dp.message_handler(Text('➖'))
async def subscribe_delete_byBtn(msg: Message):
    await subscribe_delete(msg)


@dp.message_handler(Text('Мои подписки'))
async def mysubscribes(msg: Message):
    await getSubscribes(msg)
