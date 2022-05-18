import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from states.answers import Answers
from variables import dp, check_ticker
from utils.db_api.db_work import get_currencies_info
from Exceptions.exceptions import IncorrectTicker
from Exceptions.exceptions import NotExistingCurrenciesPair
from Keyboards.markups import allCurrenciesMenu, mainMenu


@dp.message_handler(Command('getcurrencies'), state=None)
async def currencies_register(msg: Message):
    await msg.reply(text='Введите тикер первой валюты', reply_markup=allCurrenciesMenu)
    await Answers.currenciesState1.set()


@dp.message_handler(state=Answers.currenciesState1)
async def enter_first_currency(message: Message, state: FSMContext):
    answer = message.text.upper().strip()
    await state.update_data(currenciesState=answer)
    try:
        check_ticker(answer)
        async with state.proxy() as data:
            data['cur1'] = answer
        await message.reply(text='Введите тикер второй валюты')
        await Answers.currenciesState2.set()
    except IncorrectTicker as e:
        logging.info(msg=e.text)
        await message.reply(text=e.text)
        await state.finish()


@dp.message_handler(state=Answers.currenciesState2)
async def enter_second_currency(message: Message, state: FSMContext):
    answer = message.text.upper().strip()
    await state.update_data(currenciesState=answer)
    try:
        check_ticker(answer)
        async with state.proxy() as data:
            cur1 = data['cur1']
        cur2 = answer
        result = get_currencies_info(cur1, cur2)
        await message.reply(text=result, reply=False, reply_markup=mainMenu)
        await state.finish()
    except IncorrectTicker as e:
        await message.reply(text=e.text)
    except NotExistingCurrenciesPair as e:
        await message.reply(text=e.text, reply=False)
    finally:
        await state.finish()
