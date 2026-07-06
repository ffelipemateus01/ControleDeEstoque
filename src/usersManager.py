from src.database import SQLDatabase
from src.constants import DATABASE_NAME
from src.entities.user import User
from src.util import normalizeUsers

class UsersManager:
    def __init__(self):
        self.db = SQLDatabase(DATABASE_NAME)
        self.users: list[User] = normalizeUsers(self.db.getUsers())

    def createUser(self, name: str) -> User:
        id = self.db.createUser(name)
        user = User(id=id, name=name)
        self.users.append(user)

    def getUsers(self) -> list[User]:
        return self.users