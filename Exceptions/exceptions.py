class IncorrectTicker(Exception):
    def __init__(self, text):
        self.text = text


class EmptySubscribesList(Exception):
    def __init__(self):
        self.text = 'Пользователь не подписан ни на одно событие'


class NotExistingCurrenciesPair(Exception):
    def __init__(self):
        self.text = 'Я не знаю ничего про указанную валютную пару'
