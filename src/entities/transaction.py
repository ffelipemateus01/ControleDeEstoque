from dataclasses import dataclass

@dataclass
class Transaction:
    '''Entidade de movimentação de um item'''
    type: str
    itemName: str
    quantity: int
    userName: str
    date: str
    itemCode: int | None
    userId: int | None
    id: int | None