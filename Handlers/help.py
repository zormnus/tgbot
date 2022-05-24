from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from variables import dp


@dp.message_handler(Command('help'))
async def send_menu(msg: Message):
    await msg.reply(
        text='\n/addstock - Добавить акцию в список'
             '\n/deletestock - Убрать акцию из списка'
             '\n/getstocks - Просмотреть данные по всем котировкам из вашего списка'
             '\n/showstocks - Просмотреть данные по всем котировкам из вашего списка'
             '\n/getcurrencies - Получить актуальную информацию по курсу валют'
             '\n/getsubscribes - Получить информацию по подпискам на акции'
             '\nЕсли вы - новый пользователь, то просто добавляйте интересующие вас'
             ' котировки в список, изначально он пустой!',
        reply=False
    )
