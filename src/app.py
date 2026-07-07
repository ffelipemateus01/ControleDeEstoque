from src.factory import Factory
from src.exceptions import ItemException, StockException, UserException
from datetime import datetime

class StockApp:
    def __init__(self):
        self._stock = Factory.getStock()
        self._usersManager = Factory.getUsersManager()
        print('Bem vindo ao sistema de controle de estoque!')
        self.run()
        
    def run(self):
        while True:
            print('1- Listar itens no estoque')
            print('2- Movimentar item do estoque')
            print('3- Listar movimentações recentes')
            print('4- Cadastrar usuário')
            print('5- Listar usuários')
            print('0- Encerrar')
            option = input('Digite sua opção: ')
            match option:
                case '1':
                    self.showItems()
                case '2':
                    self.showMoveOptions()
                case '3':
                    self.showRecentMoves()
                case '4':
                    self.showSignUp()
                case '5':
                    self.showUsers() 
                case '0':
                    print('Encerrando...')
                    break
                case _ :
                    print('Opção inválida.')

    def showItems(self):
        if not self._stock.hasItems:
            print('Nenhum item cadastrado no estoque.')
            return
        print(f'Código     | Nome     | Quantidade')
        for item in self._stock.getItems():
            print(f'{item.code:04d}     | {item.name}     | {item.quantity}')

    def showUsers(self):
        if not self._usersManager.hasUsers:
            print('Nenhum usuário cadastrado no sistema.')
            return
        print(f'id     | Nome')
        for user in self._usersManager.getUsers():
            print(f'{user.id:04d}     | {user.name}')

    def showRecentMoves(self):
        print(f'id     | Data     | Tipo     | Item     | Quantidade     | Usuário')
        for t in self._stock.getTransactions():
            print(f'{t.id:04d}     | {t.date}    | {self.translateType(t.type)}     | {t.itemName}     | {t.quantity}     | {t.userName}')

    def showMoveOptions(self):
        print('1- Adicionar novo item')
        print('2- Adicionar item existente')
        print('3- Retirar item')
        print('0- Voltar')
        option = input('Digite sua opção: ')
        try:
            match option:
                case '1':
                    self.showCreateItem()
                case '2':
                    self.showAddItem()
                case '3':
                    self.showRmvItem()
                case '0':
                    pass
                case _:
                    print('Opção inválida! Digite uma entrada válida.')
                    self.showMoveOptions()
        except (ItemException, StockException, UserException) as e:
            print(f'Erro: {e}')

    def showCreateItem(self):
        if not self._usersManager.hasUsers:
            print('Nenhum usuário cadastrado no sistema.')
            return
        name = self.readStr('Digite o nome do item: ')
        initialQuantity = self.readInt('Digite a quantidade inicial inserida: ')
        date = datetime.now().strftime('%d/%m/%Y')
        userId = self.readUserId()
        item = Factory.getItem(name, initialQuantity)
        self._stock.insertItem(item, userId, date)
        print('Item cadastrado com sucesso!')

    def showAddItem(self):
        if not self._usersManager.hasUsers:
            print('Nenhum usuário cadastrado no sistema.')
            return
        if not self._stock.hasItems:
            print('Nenhum item cadastrado no estoque.')
            return
        self.showItems()
        while True:
            code = self.readInt('Digite o código do item: ')
            if self._stock.getItem(code) is not None:
                break
            print('Item não encontrado no sistema. Digite um código válido.')
        quantity = self.readInt('Digite a quantidade: ')
        date = datetime.now().strftime('%d/%m/%Y')
        userId = self.readUserId()
        self._stock.updateItem('in', code, quantity, userId, date)
        print('Entrada registrada com sucesso!')

    def showRmvItem(self):
        if not self._usersManager.hasUsers:
            print('Nenhum usuário cadastrado no sistema.')
            return
        if not self._stock.hasItems:
            print('Nenhum item cadastrado no estoque.')
            return
        self.showItems()
        code = self.readInt('Digite o código do item: ')
        quantity = self.readInt('Digite a quantidade: ')
        date = datetime.now().strftime('%d/%m/%Y')
        userId = self.readUserId()
        self._stock.updateItem('out', code, quantity, userId, date)
        print('Saída registrada com sucesso!')
    
    def showSignUp(self):
        name = self.readStr('Digite o nome do usuário: ')
        self._usersManager.createUser(name)
        print('Usuário cadastrado com sucesso!')

    def translateType(self, type: str) -> str:
        if type == 'in':
            return 'Entrada'
        else:
            return 'Saída'
        
    def readInt(self, message: str) -> int:
        while True:
            value = input(message).strip()
            try:
                return int(value)
            except ValueError:
                print('Valor inválido. Digite apenas números inteiros.')

    def readStr(self, message: str) -> str:
        while True:
            value = input(message).strip()
            if value:
                return value
            print('O campo não pode ficar vazio')

    def readUserId(self) -> int:
        self.showUsers()
        while True:
            userId = self.readInt('Digite seu id de usuário: ')
            if self._usersManager.getUser(userId) is not None:
                return userId
            print('Usuário não encontrado! Informe um id da lista acima.')