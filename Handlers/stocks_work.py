import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from Keyboards.markups import stocksMenu, allStocksMenu
from states.answers import Answers
from utils.users_work import add_ticker, delete_ticker
from variables import dp, check_ticker
from utils.db_api.db_work import get_stocks_info
from Exceptions.exceptions import IncorrectTicker, EmptySubscribesList


@dp.message_handler(Command('addstock'), state=None)
async def addstock_register(msg: Message):
    await msg.reply('Введите тикер компании', reply=False, reply_markup=allStocksMenu)
    await Answers.addStockState.set()


@dp.message_handler(state=Answers.addStockState)
async def _enter_stock_ticker_add(message: Message, state: FSMContext):
    answer = message.text.upper().strip()
    await state.update_data(addStockState=answer)
    try:
        check_ticker(answer, currencies=False)
        add_ticker(message.from_user.id, answer)
        await message.reply(text=f'Успешно добавил котировки компании {answer} в ваш список!'
                            , reply_markup=stocksMenu)
    except IncorrectTicker as e:
        await message.reply(text=e.text, reply_markup=stocksMenu)
    finally:
        await state.finish()


@dp.message_handler(Command('deletestock'), state=None)
async def deletestock_register(msg: Message):
    await msg.reply('Введите тикер компании', reply=False, reply_markup=allStocksMenu)
    await Answers.deleteStockState.set()


@dp.message_handler(state=Answers.deleteStockState)
async def _enter_stock_ticker_delete(message: Message, state: FSMContext):
    answer = message.text.upper().strip()
    await state.update_data(deleteStockState=answer)
    try:
        check_ticker(answer, currencies=False)
        delete_ticker(message.from_user.id, answer)
        await message.reply(text=f'Успешно удалил котировки компании {answer} из вашего списка!'
                            , reply_markup=stocksMenu)
        await state.finish()
    except IncorrectTicker as e:
        await message.reply(text=e.text, reply_markup=stocksMenu)
        await state.finish()


@dp.message_handler(Command('showstocks'), state=None)
async def showstocks_register(msg: Message):
    try:
        stocks_info = get_stocks_info(msg.from_user.id)
        for s in stocks_info:
            await msg.reply(text=s, reply=False)
    except EmptySubscribesList as e:
        logging.info(msg=e.text)
        await msg.reply(text='Ваш список ценных бумаг пока что пуст', reply=False, reply_markup=stocksMenu)
