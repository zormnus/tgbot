from aiogram.dispatcher.filters.state import StatesGroup, State


class Answers(StatesGroup):
    addStockState = State()
    deleteStockState = State()
    showStocksState = State()
    currenciesState1 = State()
    currenciesState2 = State()
    subscribesAddState1 = State()
    subscribesAddState2 = State()
    subscribesDeleteState1 = State()
    subscribesDeleteState2 = State()
