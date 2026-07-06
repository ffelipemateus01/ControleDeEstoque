from dataclasses import dataclass

@dataclass
class Item:
    name: str
    quantity: int
    code: int | None = None