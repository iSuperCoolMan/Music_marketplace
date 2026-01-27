import sqlite3

from sqlite3 import Cursor


def set_connection(func):
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect('frontend/my_database.db')
        cursor = connection.cursor()

        result = func(cursor, *args, **kwargs)

        connection.commit()
        connection.close()

        return result

    return wrapper


@set_connection
def start(cursor: Cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cart (
        id TEXT PRIMARY KEY,
        count INTEGER
        )
        ''')


@set_connection
def insert_into_cart(cursor: Cursor, id: str, count: int = 1):
    cursor.execute('SELECT * FROM Cart')

    cart = {item[0]: item[1] for item in cursor.fetchall()}

    print("database before", cart)

    if id in cart.keys():
        value = cart[id] + count

        if value <= 0:
            cursor.execute('DELETE FROM Cart WHERE id = ?', (id,))
        else:
            cursor.execute('UPDATE Cart SET count = ? WHERE id = ?', (value, id))
    else:
        if count > 0:
            cursor.execute('INSERT INTO Cart (id, count) VALUES (?, ?)', (id, count))
        else:
            raise ValueError

    cursor.execute('SELECT * FROM Cart')
    print("database after", cursor.fetchall())


@set_connection
def get_count_from_cart(cursor: Cursor, id: str):
    cursor.execute('SELECT * FROM Cart')
    cart = {item[0]: item[1] for item in cursor.fetchall()}
    return cart[id]


@set_connection
def get_ids_from_cart(cursor: Cursor):
    cursor.execute('SELECT * FROM Cart')

    return [item[0] for item in cursor.fetchall()]


start()