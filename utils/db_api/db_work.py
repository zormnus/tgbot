import sqlite3
from Exceptions.exceptions import EmptySubscribesList, NotExistingCurrenciesPair


def _check_tables(country: str = None, connect: sqlite3.Connection = None):
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS CurrenciesTable(
        name VARCHAR(255) NOT NULL,
        last_price REAL,
        change_percents VARCHAR(255),
        change REAL,
        bid REAL,
        ask REAL,
        max_value REAL,
        min_value REAL,
        technical_rating VARCHAR(255)
    )""")
    connect.commit()
    if country is not None:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {country}StocksTable(
            ticker TEXT NOT NULL,
            full_name TEXT NOT NULL,
            last_price TEXT,
            change TEXT,
            change_percents TEXT,
            volume TEXT
        )""")
        connect.commit()


def update_currencies_table(data: list):
    with sqlite3.connect('investments.db', check_same_thread=True) as conn:
        cursor = conn.cursor()
        _check_tables(connect=conn)
        cursor.execute(f"""UPDATE CurrenciesTable SET last_price=?,
        change_percents=?,
        change=?,
        bid=?,
        ask=?,
        max_value=?,
        min_value=?,
        technical_rating=? WHERE name=?
        """, (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], f'{data[0][0:3]}/{data[0][3:6]}'))
        conn.commit()


def update_Russia_stocks_table(data: list):
    with sqlite3.connect('investments.db', check_same_thread=True) as conn:
        cursor = conn.cursor()
        _check_tables(country='Russia', connect=conn)
        cursor.execute(f"""UPDATE RussiaStocksTable SET full_name=?,
        last_price=?,
        change=?,
        change_percents=?,
        volume=? WHERE ticker=?
        """, (data[0], data[1], data[3], data[2], data[5], data[6]))
        conn.commit()


def start_russia(data: list):
    with sqlite3.connect('investments.db', check_same_thread=True) as conn:
        cursor = conn.cursor()
        _check_tables(country='Russia', connect=conn)
        cursor.execute(f"""INSERT INTO RussiaStocksTable
            VALUES (?,?,?,?,?,?)
            """, (data[6], data[0], data[1], data[3], data[2], data[5]))
        conn.commit()


def start_usa(data: list):
    with sqlite3.connect('investments.db', check_same_thread=True) as conn:
        cursor = conn.cursor()
        _check_tables(country='Usa', connect=conn)
        cursor.execute(f"""INSERT INTO UsaStocksTable
            VALUES (?,?,?,?,?,?)
            """, (data[0], data[1], data[2], data[3], data[4], data[5]))
        conn.commit()


def start_currencies(data: list):
    with sqlite3.connect('investments.db', check_same_thread=True) as conn:
        cursor = conn.cursor()
        _check_tables(connect=conn)
        cursor.execute(f"""INSERT INTO CurrenciesTable
            VALUES (?,?,?,?,?,?,?,?,?)
            """, (
            f"{data[0][0:3]}/{data[0][3:6]}", data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[1]))


def update_USA_stocks_table(data: list):
    with sqlite3.connect('investments.db', check_same_thread=True) as conn:
        cursor = conn.cursor()
        _check_tables(country='Usa', connect=conn)
        cursor.execute(f"""UPDATE UsaStocksTable SET full_name=?,
        last_price=?,
        change=?,
        change_percents=?,
        volume=? WHERE ticker=?
        """, (data[1], data[2], data[3], data[4], data[5], data[0]))


def get_currencies_info(ticker1: str, ticker2: str) -> str:
    s = f'{ticker1}/{ticker2}'
    with sqlite3.connect('investments.db', check_same_thread=True) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM CurrenciesTable WHERE name LIKE '{s}%'""")
        result = cursor.fetchone()
        if result is None:
            raise NotExistingCurrenciesPair
        return f'💵Курс {result[0]}:' \
               f'\n\tТекущая цена: {result[1]}' \
               f'\n\tИзменение в %: {result[2]}' \
               f'\n\tИзменение в значении: {result[3]}' \
               f'\n\tБИД(цена спроса): {result[4]}' \
               f'\n\tАСК(цена предложения): {result[5]}' \
               f'\n\tМаксимальное значение за день: {result[6]}' \
               f'\n\tМинимальное значение за день: {result[7]}' \
               f'\n\tТехнический рейтинг: {result[8]}\n'


def get_all_currencies_tickers() -> list:
    with sqlite3.connect('investments.db', check_same_thread=True) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT name FROM CurrenciesTable""")
        notes = cursor.fetchall()
        result = [note[0][0:3] for note in notes]
        return list(set(result))


def get_all_stocks_tickers() -> list:
    with sqlite3.connect('investments.db', check_same_thread=True) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT ticker FROM UsaStocksTable""")
        USANotes = cursor.fetchall()
        cursor.execute("""SELECT ticker FROM RussiaStocksTable""")
        RussiaNotes = cursor.fetchall()
        USANotes = [note[0] for note in USANotes]
        RussiaNotes = [note[0] for note in RussiaNotes]
        return USANotes + RussiaNotes


def get_stocks_info(user_id: str) -> list:
    from utils.users_work import get_subscribes_tickers
    tickers = get_subscribes_tickers(user_id)
    if not tickers:
        raise EmptySubscribesList
    with sqlite3.connect('investments.db') as conn:
        cursor = conn.cursor()
        counter: int = 1
        result = []
        for ticker in tickers:
            cursor.execute(f"""SELECT * FROM RussiaStocksTable WHERE ticker = '{ticker}'""")
            rusData = cursor.fetchone()
            if rusData is not None:
                s = f"{counter}) 🇷🇺{rusData[0]}" \
                    f"\nПолное название: {rusData[1]}" \
                    f"\nСтоимость: {rusData[2]}" \
                    f"\nИзменение в %: {rusData[4]}" \
                    f"\nИзменение в RUB: {rusData[3]}" \
                    f"\nОбъём торгов: {rusData[5]}"
            else:
                cursor.execute(f"""SELECT * FROM UsaStocksTable WHERE ticker = '{ticker}'""")
                usaData = cursor.fetchone()
                s = f"{counter}) 🇺🇸{usaData[0]}" \
                    f"\nПолное название: {usaData[1]}" \
                    f"\nСтоимость: {usaData[2]}" \
                    f"\nИзменение в %: {usaData[4]}" \
                    f"\nИзменение в USD: {usaData[3]}" \
                    f"\nОбъём торгов: {usaData[5]}"
            counter += 1
            result.append(s)
        return result


def get_stock_price(ticker: str) -> float:
    with sqlite3.connect('investments.db') as conn:
        cursor = conn.cursor()
        result = cursor.execute(f"""SELECT last_price FROM UsaStocksTable WHERE ticker = '{ticker}'""").fetchone()
        if result is None:
            result = cursor.execute(f"""SELECT last_price FROM RussiaStocksTable WHERE ticker = '{ticker}'""").fetchone()
            return result[0][0:-3]
        return result[0]
