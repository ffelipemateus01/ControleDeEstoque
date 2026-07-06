from sqlite3 import Error

class StockException(Error):
    pass

class UserException(Error):
    pass

class ItemException(Error):
    pass