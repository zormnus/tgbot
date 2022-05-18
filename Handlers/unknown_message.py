from aiogram.types import Message
from variables import dp


@dp.message_handler()
async def unknown_msg(msg: Message):
    await msg.reply('Неизвестная команда! Попробуйте ещё раз'
                    '\nВведите команду /help чтобы узнать о возможностях бота',
                    reply=False)
