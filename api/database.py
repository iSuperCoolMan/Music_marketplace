import sqlite3

from sqlite3 import Cursor

from api.models import Product


def set_connection(func):
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect('api/my_database.db')
        cursor = connection.cursor()

        result = func(cursor, *args, **kwargs)

        connection.commit()
        connection.close()

        return result

    return wrapper


@set_connection
def start(cursor: Cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        username TEXT PRIMARY KEY,
        hashed_password TEXT
        )
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
        id TEXT PRIMARY KEY,
        name TEXT,
        seller TEXT,
        price INTEGER,
        stock INTEGER
        )
        ''')


@set_connection
def create_user(cursor: Cursor, username: str, hashed_password: str):
    users = [item[0] for item in cursor.fetchall()]

    if username in users:
        raise ValueError
    else:
        cursor.execute(
            'INSERT INTO Users (username, hashed_password) VALUES (?, ?)',
            (username, hashed_password)
        )


@set_connection
def get_user(cursor: Cursor, username: str):
    cursor.execute('SELECT * FROM Users')

    users = {item[0]: {
        "username": item[0],
        "hashed_password": item[1]
    } for item in cursor.fetchall()}

    if username in users.keys():
        return users[username]
    else:
        raise ValueError


@set_connection
def get_all_products(cursor: Cursor):
    cursor.execute('SELECT * FROM Products')

    return [{
        "id": item[0],
        "name": item[1],
        "seller": item[2],
        "price": item[3],
        "stock": item[4]
    } for item in cursor.fetchall()]


@set_connection
def get_products_by_username(cursor: Cursor, username: str):
    cursor.execute('SELECT * FROM Products WHERE seller = ?', (username,))

    return [{
        "id": item[0],
        "name": item[1],
        "seller": item[2],
        "price": item[3],
        "stock": item[4]
    } for item in cursor.fetchall()]


@set_connection
def get_product(cursor: Cursor, id: str):
    cursor.execute('SELECT * FROM Products')

    products = {item[0]: {
        "id": item[0],
        "name": item[1],
        "seller": item[2],
        "price": item[3],
        "stock": item[4]
    } for item in cursor.fetchall()}

    if id in products.keys():
        return products[id]
    else:
        raise ValueError


@set_connection
def post_product(cursor: Cursor, name: str, seller: str, price: int, count: int):
    product = Product(name, None, price, count)

    cursor.execute(
        'INSERT INTO Products (id, name, seller, price, stock) VALUES (?, ?, ?, ?, ?)',
        (product.id, name, seller, price, count)
    )


start()