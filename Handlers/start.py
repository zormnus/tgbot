from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from variables import dp
from utils.users_work import check_user
from Keyboards.markups import mainMenu
from utils.monitoring import subscribes_monitoring


@dp.message_handler(Command('start'))
async def say_hello(message: Message):
    await message.reply(f'\tПривет, {message.from_user.first_name}!\nЧем могу помочь?\n',
                        reply=False, reply_markup=mainMenu)
    check_user(message.from_user.id, message.from_user.first_name)
    await subscribes_monitoring(message.from_user.id)
