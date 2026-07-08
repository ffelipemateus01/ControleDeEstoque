from src.database import SQLDatabase
from src.constants import DATABASE_NAME
from src.entities.item import Item
from src.entities.transaction import Transaction
from src.exceptions import ItemException
from src.util import normalizeItems, normalizeTransactions

class Stock:
    '''Gerenciador do estoque de itens'''
    def __init__(self):
        #conexão com o db
        self.db = SQLDatabase(DATABASE_NAME)
        #itens no estoque
        self.items: list[Item] = normalizeItems(self.db.getItems())

    def getItem(self, code: int) -> Item | None:
        '''Retorna um item a partir do código fornecido'''
        for item in self.items:
            if item.code == code:
                return item
        #não existe um item com o código fornecido
        return None

    def getItemByName(self, name: str) -> Item | None:
        '''Seleciona um item a partir do nome fornecido'''
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
        #não existe um item com o nome fornecido
        return None
    
    def insertItem(self, item: Item, userId: int, date: str):
        '''Insere um item no estoque'''
        #checka se a quantidade é válida
        if item.quantity <= 0:
            raise ItemException('A quantidade inicial deve ser maior que zero.')
        item.code = self.db.createItem(name=item.name, initialQuantity=item.quantity, userId=userId, date=date)
        self.items.append(item)

    def updateItem(self, type: str, code: int, quantity: int, userId: int, date: str):
        '''Movimenta um item que existe no estoque'''
        #checka se a quantidade é valida
        if quantity <= 0:
            raise ItemException('Para movimentar, a quantidade deve ser maior que zero.')
        #checka se o item existe
        if self.getItem(code) is None:
            raise ItemException('Não existe item cadastrado com esse código.')
        newQuantity = self.db.updateItemInStock(type=type, code=code, quantity=quantity, userId=userId, date=date)
        for i in range(0, len(self.items)):
            if self.items[i].code == code:
                #atualiza a nova quantidade no estoque
                self.items[i].quantity = newQuantity
                return

    def getItems(self) -> list[Item]:
        '''Retorna a lista de itens no estoque'''
        return self.items
    
    def getTransactions(self) -> list[Transaction]:
        '''Retorna as movimentações recentes no estoque'''
        return normalizeTransactions(self.db.getTransactions())
    
    @property
    def hasItems(self) -> bool:
        '''Verifica se existem itens no estoque'''
        return len(self.items) > 0