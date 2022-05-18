from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from Exceptions.exceptions import IncorrectTicker
from states.answers import Answers
from variables import dp
from utils.users_work import subscribe_price_add, subscribes_price_delete, get_subscribes_and_prices, get_subscribes_tickers

__first_answer = ''


@dp.message_handler(Command('subscribeadd'))
async def subscribe_add(message: Message):
    await message.reply(text='Введите тикер акции из своего списка, '
                             'на цену которой вы хотите подписаться', reply=False)
    await Answers.subscribesAddState1.set()


@dp.message_handler(state=Answers.subscribesAddState1)
async def enter_Stock(message: Message, state: FSMContext):
    answer = message.text.upper().strip()
    try:
        tickers = get_subscribes_tickers(message.from_user.id)
        if answer not in tickers:
            await message.reply(f'Вы не отслеживаете котировки компании {answer}')
            await state.finish()
            return
        async with state.proxy() as data:
            data['stockname'] = answer
        await message.reply(text='Введите цену которую хотите добавить')
        await Answers.subscribesAddState2.set()
    except IncorrectTicker as e:
        await message.reply(text=e.text)
        await state.finish()


@dp.message_handler(state=Answers.subscribesAddState2)
async def enter_price(message: Message, state: FSMContext):
    try:
        answer = float(message.text.strip())
        async with state.proxy() as data:
            stockName = data['stockname']
        subscribe_price_add(message.from_user.id, stockName, answer)
        await message.reply(text=f'Я обязательно напомню вам о достижении этой цены котировками компании {stockName}')
    except ValueError as e:
        await message.reply(text='Введено некорректное значение')
    finally:
        await state.finish()


@dp.message_handler(Command('subscribedelete'))
async def subscribe_delete(message: Message):
    await message.reply(text='Введите тикер акции из своего списка, '
                             'подписку на цену которой вы хотите удалить', reply=False)
    await Answers.subscribesDeleteState1.set()


@dp.message_handler(state=Answers.subscribesDeleteState1)
async def enter_Stock_delete(message: Message, state: FSMContext):
    answer = message.text.upper().strip()
    try:
        tickers = get_subscribes_tickers(message.from_user.id)
        if answer not in tickers:
            await message.reply(f'Вы не отслеживаете котировки компании {answer}')
            await state.finish()
            return
        async with state.proxy() as data:
            data['stockname'] = answer
        await message.reply(text='Введите цену которую хотите удалить')
        await Answers.subscribesDeleteState2.set()
    except IncorrectTicker as e:
        await message.reply(text=e.text)
        await state.finish()


@dp.message_handler(state=Answers.subscribesDeleteState2)
async def enter_price_delete(message: Message, state: FSMContext):
    try:
        answer = float(message.text.strip())
        async with state.proxy() as data:
            stockName = data['stockname']
        subscribes_price_delete(message.from_user.id, stockName, answer)
        await message.reply(text=f'Успешно удалил вашу подписку')
    except ValueError as e:
        await message.reply(text='Введено некорректное значение')
    finally:
        await state.finish()


@dp.message_handler(Command('getsubscribes'))
async def getSubscribes(msg: Message):
    answer = get_subscribes_and_prices(msg.from_user.id)
    if answer == {}:
        await msg.reply(text='Ваш список подписок пока что пуст', reply=False)
        return
    s = ""
    for ticker, prices in answer.items():
        if prices:
            s += f"{ticker} : {[price[1] for price in prices]}\n"
    await msg.reply(text=s, reply=False)
