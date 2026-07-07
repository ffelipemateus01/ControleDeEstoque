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
    
    def getUser(self, id: int) -> User | None:
        for user in self.users:
            if user.id == id:
                return user
        return None
    
    def getUserByName(self, name: str) -> User | None:
        for user in self.users:
            if user.name.lower() == name.lower():
                return user
        return None
    
    @property
    def hasUsers(self) -> bool:
        return len(self.users) > 0