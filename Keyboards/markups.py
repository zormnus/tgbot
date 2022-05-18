from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from variables import existing_stocks_tickers, existing_currencies_tickers

mainButtons = KeyboardButton('Главное меню')


stocksButton = KeyboardButton('Акции📊')
currenciesButton = KeyboardButton('Валюты💵')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(stocksButton, currenciesButton)


addStockButton = KeyboardButton('Добавить акцию в ваш список')
deleteStockButton = KeyboardButton('Удалить акцию из вашего списка')
showStocksButton = KeyboardButton('Показать текущую информацию по вашим акциям')
back_button = KeyboardButton('В главное меню◀️')
to_subscribes_button = KeyboardButton('Уведомить о достижении цены')
stocksMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(addStockButton, deleteStockButton).add(showStocksButton) \
    .add(back_button).add(to_subscribes_button)


addSubscribeButton = KeyboardButton('➕')
delSubscribeButton = KeyboardButton('➖')
showSubscribesButton = KeyboardButton('Мои подписки')
subscribesMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(addSubscribeButton, delSubscribeButton
                                                               , showSubscribesButton, back_button)


allStocksMenu = ReplyKeyboardMarkup(resize_keyboard=True)
allStocksMenu.add(back_button)
for stock in existing_stocks_tickers:
    tickerBtn = KeyboardButton(stock)
    allStocksMenu.add(tickerBtn)


allCurrenciesMenu = ReplyKeyboardMarkup(resize_keyboard=True)
allCurrenciesMenu.add(back_button)
for currency in existing_currencies_tickers:
    tickerBtn = KeyboardButton(currency)
    allCurrenciesMenu.add(tickerBtn)
