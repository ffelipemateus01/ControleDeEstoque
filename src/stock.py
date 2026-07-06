from src.database import SQLDatabase
from src.constants import DATABASE_NAME
from src.entities.item import Item
from src.entities.transaction import Transaction
from src.util import normalizeItems, normalizeTransactions

class Stock:
    def __init__(self):
        self.db = SQLDatabase(DATABASE_NAME)
        self.items: list[Item] = normalizeItems(self.db.getItems())

    def getItem(self, code: int) -> Item | None:
        for item in self.items:
            if item.code == code:
                return item
        return None

    def insertItem(self, item: Item, userId: int):
        item.code = self.db.createItem(name=item.name, initialQuantity=item.quantity, userId=userId)
        self.items.append(item)

    def updateItem(self, type: str, code: int, quantity: int, userId: int):
        if quantity <= 0:
            print('O valor inserido para o campo *Quantidade* é inválido!')
            return
        newQuantity = self.db.updateItemInStock(type=type, code=code, quantity=quantity, userId=userId)
        for i in range(0, len(self.items)):
            if self.items[i].code == code:
                self.items[i].quantity = newQuantity
                return

    def getItems(self) -> list[Item]:
        return self.items
    
    def getTransactions(self) -> list[Transaction]:
        return normalizeTransactions(self.db.getTransactions())