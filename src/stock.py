from src.database import SQLDatabase
from src.constants import DATABASE_NAME
from src.entities.item import Item
from src.entities.transaction import Transaction
from src.exceptions import ItemException
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

    def insertItem(self, item: Item, userId: int, date: str):
        if item.quantity <= 0:
            raise ItemException('A quantidade inicial deve ser maior que zero.')
        item.code = self.db.createItem(name=item.name, initialQuantity=item.quantity, userId=userId, date=date)
        self.items.append(item)

    def updateItem(self, type: str, code: int, quantity: int, userId: int, date: str):
        if quantity <= 0:
            raise ItemException('Para movimentar, a quantidade deve ser maior que zero.')
        if self.getItem(code) is None:
            raise ItemException('Não existe item cadastrado com esse código.')
        newQuantity = self.db.updateItemInStock(type=type, code=code, quantity=quantity, userId=userId, date=date)
        for i in range(0, len(self.items)):
            if self.items[i].code == code:
                self.items[i].quantity = newQuantity
                return

    def getItems(self) -> list[Item]:
        return self.items
    
    def getTransactions(self) -> list[Transaction]:
        return normalizeTransactions(self.db.getTransactions())
    
    @property
    def hasItems(self) -> bool:
        return len(self.items) > 0