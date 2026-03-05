from pydantic import BaseModel
import uuid


class BaseProduct(BaseModel):
    uuid: uuid.UUID
    price: int
    name: str


class Product:
    __id: str
    __name: str
    __image: None
    __price: int
    __stock: int

    def __init__(self, name, image, price, stock):
        self.__id = str(self.__hash__())
        self.__name = name
        self.__image = image
        self.__price = price
        self.__stock = stock

    @property
    def id(self):
        return self.__id

    def get_info(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "image": self.__image,
            "price": self.__price,
            "stock": self.__stock
        }

    def buy(self):
        self.__stock -= 1

    def collect(self, count):
        self.__stock += count


class Cart:
    __products: dict[int: Product]

    def __init__(self):
        self.__products = {}

    def add_product(self, product: Product):
        self.__products[product.id] = product

    def remove_product(self, id: int):
        self.__products.pop(id)


class User:
    __id: int
    __login: str
    __password: str
    __last_ip: str
    __cart: Cart

    def __init__(self, login, password):
        self.__id = self.__hash__()
        self.__login = login
        self.__password = password
        self.__cart = Cart()

    @property
    def id(self):
        return self.__id

    @property
    def login(self):
        return self.__login

    @property
    def password(self):
        return self.__password

    def set_ip(self, ip: str):
        self.__last_ip = ip