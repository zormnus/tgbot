from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Начать работу с ботом'),
            types.BotCommand('help', 'Справочная информация'),
            types.BotCommand('addstock', 'Добавить акцию в список'),
            types.BotCommand('deletestock', 'Убрать акцию из списка'),
            types.BotCommand('showstocks', 'Просмотреть данные по всем '
                                          'котировкам из вашего списка'),
            types.BotCommand('getcurrencies', 'Получить актуальную информацию '
                                              'по курсу валют'),
            types.BotCommand('getsubscribes', 'Получить информацию по подпискам '
                                              'на цены активов')
        ]
    )
