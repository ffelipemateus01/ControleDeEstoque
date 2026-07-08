from src.database import SQLDatabase
from src.constants import DATABASE_NAME
from src.entities.user import User
from src.util import normalizeUsers

class UsersManager:
    '''Gerenciador de usuários do sistema'''
    def __init__(self):
        #conexão com o db
        self.db = SQLDatabase(DATABASE_NAME)
        #lista de usuários no sistema
        self.users: list[User] = normalizeUsers(self.db.getUsers())

    def createUser(self, name: str) -> User:
        '''Cadastra um novo usuário'''
        id = self.db.createUser(name)
        user = User(id=id, name=name)
        self.users.append(user)

    def getUsers(self) -> list[User]:
        '''Retorna a lista de usuários no sistema'''
        return self.users
    
    def getUser(self, id: int) -> User | None:
        '''Retorna um usuário a partir do id fornecido'''
        for user in self.users:
            if user.id == id:
                return user
        #não existe um usuário com o id fornecido
        return None
    
    def getUserByName(self, name: str) -> User | None:
        '''Seleciona um usuário a partir do nome'''
        for user in self.users:
            if user.name.lower() == name.lower():
                return user
        #não existe um usuário com o nome fornecido
        return None
    
    @property
    def hasUsers(self) -> bool:
        '''Verifica se existem usuários cadastrados no sistema'''
        return len(self.users) > 0