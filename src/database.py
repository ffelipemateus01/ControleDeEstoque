import sqlite3
from src.exceptions import ItemException, StockException, UserException

class SQLDatabase:
    def __init__(self, dbName: str):
        self.connection = sqlite3.connect(dbName)
        self.cursor = self.connection.cursor()
        self.cursor.execute('PRAGMA foreign_keys = ON')
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS items (
                code INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS stock(
                itemCode INTEGER NOT NULL UNIQUE,
                quantity INTEGER NOT NULL CHECK(quantity >= 0),
                FOREIGN KEY(itemCode) REFERENCES items(code));
            CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                itemCode INTEGER NOT NULL, 
                quantity INTEGER NOT NULL,
                userId INTEGER NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY(itemCode) REFERENCES items(code),
                FOREIGN KEY(userId) REFERENCES users(id));
            ''')
        self.connection.commit()

    def createUser(self, name: str) -> int:
        try:
            (userId, ) = self.cursor.execute('''
                INSERT INTO users (name)
                VALUES (?)
                RETURNING id
            ''', (name,)).fetchone()
            self.connection.commit()
            return userId
        except sqlite3.Error:
            raise UserException('Houve um erro ao tentar inserir um usuário.')

    def getUsers(self) -> list[dict]:
        try:
            users = []
            results = self.cursor.execute('''
                SELECT * FROM users
            ''').fetchall()
            for r in results:
                user = {}
                user['id'] = r[0]
                user['name'] = r[1]
                users.append(user)
            return users
        except sqlite3.Error:
            raise UserException('Houve um erro ao tentar listar os usuários.')
        
    def createItem(self, name: str, initialQuantity: int, userId: int, date: str) -> int:
        try:
            (code, ) = self.cursor.execute('''
                INSERT INTO items (name)
                VALUES (?)
                RETURNING code
            ''', (name,)).fetchone()
            self.updateItemInStock('in', code, initialQuantity, userId, date)
            return code
        except sqlite3.Error:
            self.connection.rollback()
            raise ItemException('Houve um erro ao tentar inserir um item no estoque.')
        
    def updateItemInStock(self, type: str, code: int, quantity: int, userId: int, date: str) -> int:
        try:
            if type == 'in':
                (newQuantity,) = self.cursor.execute('''
                    INSERT INTO stock (itemCode, quantity)
                    VALUES (?, ?)
                    ON CONFLICT(itemCode) DO UPDATE
                    SET quantity=quantity + excluded.quantity
                    RETURNING quantity''', (code, quantity)).fetchone()
            else:
                result = self.cursor.execute('''
                    UPDATE stock
                    SET quantity=quantity - ?
                    WHERE itemCode = ?
                    RETURNING quantity''', (quantity, code)).fetchone()
                if result is None:
                    raise ItemException('Item não encontrado no estoque.')
                (newQuantity,) = result
            self.newTransaction(type, code, quantity, userId, date)
            self.connection.commit()
            return newQuantity
        except sqlite3.IntegrityError:
            self.connection.rollback()
            raise ItemException('Quantidade em estoque insuficiente para esta saída.')
        except ItemException:
            self.connection.rollback()
            raise
        except sqlite3.Error:
            self.connection.rollback()
            raise ItemException('Houve um erro ao tentar movimentar um item.')
        
    def getItems(self) -> list[dict]:
        try:
            items = []
            results = self.cursor.execute('''
                SELECT i.code AS Código, i.name AS Item, s.quantity AS Quantidade 
                FROM stock AS s
                INNER JOIN items AS i
                ON i.code=s.itemCode
            ''').fetchall()
            for r in results:
                item = {}
                item['code']=r[0]
                item['name']=r[1]
                item['quantity']=r[2]
                items.append(item)
            return items
        except sqlite3.Error:
            raise StockException('Houve um erro ao tentar listar os itens no estoque.')
        
    def newTransaction(self, type: str, itemCode: int, quantity: int, userId: int, date: str):
        self.cursor.execute('''
            INSERT INTO transactions (type, itemCode, quantity, date, userId)
            VALUES (?, ?, ?, ?, ?)''', (type, itemCode, quantity, date, userId))
        
    def getTransactions(self) -> list[dict]:
        try:
            transactions = []
            results = self.cursor.execute('''
                SELECT t.id, t.type, i.code, i.name, t.quantity, u.name, u.id, t.date FROM transactions AS t
                INNER JOIN items AS i
                ON i.code = t.itemCode 
                INNER JOIN users AS u
                ON u.id = t.userId
                ORDER BY t.id DESC
            ''')
            for r in results:
                transaction = {}
                transaction['id'] = r[0]
                transaction['type'] = r[1]
                transaction['itemCode'] = r[2]
                transaction['itemName'] = r[3]
                transaction['quantity'] = r[4]
                transaction['userName'] = r[5]
                transaction['userId'] = r[6]
                transaction['date'] = r[7]
                transactions.append(transaction)
            return transactions
        except sqlite3.Error:
            raise StockException('Houve um erro ao tentar listar as transações no sistema.')

    def close(self):
        return self.connection.close()
        