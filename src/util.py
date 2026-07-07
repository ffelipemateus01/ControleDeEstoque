from src.entities.item import Item
from src.entities.user import User
from src.entities.transaction import Transaction

def normalizeItems(items: list[dict]) -> list[Item]:
    normalizedItems = []
    for item in items:
        normalizedItems.append(Item(code=item['code'], name=item['name'], quantity=item['quantity']))
    return normalizedItems

def normalizeUsers(users: list[dict]) -> list[User]:
    normalizedUsers = []
    for user in users:
        normalizedUsers.append(User(name=user['name'], id=user['id']))
    return normalizedUsers

def normalizeTransactions(transactions: list[dict]) -> list[Transaction]:
    normalizedTransactions = []
    for transaction in transactions:
        normalizedTransactions.append(Transaction(type=transaction['type'], 
                                                  itemName=transaction['itemName'], 
                                                  quantity=transaction['quantity'], 
                                                  userName=transaction['userName'], 
                                                  itemCode=transaction['itemCode'], 
                                                  date=transaction['date'],
                                                  userId=transaction['userId'], 
                                                  id=transaction['id']))
    return normalizedTransactions