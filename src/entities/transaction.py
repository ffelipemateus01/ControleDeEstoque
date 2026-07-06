from dataclasses import dataclass

@dataclass
class Transaction:
    type: str
    itemName: str
    quantity: int
    userName: str
    itemCode: int | None
    userId: int | None
    id: int | None