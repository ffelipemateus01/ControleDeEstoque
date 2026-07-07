from src.entities.item import Item
from src.entities.user import User
from src.stock import Stock
from src.usersManager import UsersManager
from src.database import SQLDatabase
from src.constants import DATABASE_NAME

class Factory:
    @staticmethod
    def getItem(name: str, quantity: int, code: int | None = None) -> Item:
        return Item(code=code, name=name, quantity=quantity)

    @staticmethod
    def getUser(name: str, id: int | None = None) -> User:
        return User(id=id, name=name)
    
    @staticmethod
    def getTransaction(name: str) -> User:
        return User(name)

    @staticmethod
    def getStock() -> Stock:
        return Stock()
    
    @staticmethod
    def getUsersManager() -> UsersManager:
        return UsersManager()
    
    @staticmethod
    def getDatabase() -> SQLDatabase:
        return SQLDatabase(DATABASE_NAME)