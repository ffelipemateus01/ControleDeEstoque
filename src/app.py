from src.factory import Factory

class StockApp:
    def __init__(self):
        self._stock = Factory.getStock()
        self._usersManager = Factory.getUsersManager()
        print('Bem vindo ao sistema de controle de estoque!')
        self.showMenu()
        
    def showMenu(self):
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
                return
            case _ :
                print('Opção inválida.')
        self.showMenu()

    def showItems(self):
        print(f'Código     | Nome     | Quantidade')
        for item in self._stock.getItems():
            print(f'{item.code:04d}     | {item.name}     | {item.quantity}')

    def showUsers(self):
        print(f'id     | Nome     ')
        for user in self._usersManager.getUsers():
            print(f'{user.id:04d}     | {user.name}')

    def translateType(self, type: str) -> str:
        if type == 'in':
            return 'Entrada'
        else:
            return 'Saída'

    def showRecentMoves(self):
        print(f'id     | Tipo     | Item     | Quantidade     | Usuário     ')
        for transaction in self._stock.getTransactions():
            print(f'{transaction.id:04d}     | {self.translateType(transaction.type)}     | {transaction.itemName}     | {transaction.quantity}     | {transaction.userName}     ')

    def showMoveOptions(self):
        print('1- Adicionar novo item')
        print('2- Adicionar item existente')
        print('3- Retirar item')
        print('0- Voltar')
        option = input('Digite sua opção: ')
        match option:
            case '1':
                name = input('Digite o nome do item: ')
                initialQuantity = int(input('Digite a quantidade inicial inserida: '))
                self.showUsers()
                userId = int(input('Digite seu id de usuário: '))
                item = Factory.getItem(name, initialQuantity)
                self._stock.insertItem(item, userId)
            case '2':
                self.showItems()
                code = int(input('Digite o código do item: '))
                quantity = int(input('Digite a quantidade: '))
                self.showUsers()
                userId = int(input('Digite seu id de usuário: '))
                self._stock.updateItem('in', code, quantity, userId)
            case '3':
                self.showItems()
                code = int(input('Digite o código do item: '))
                quantity = int(input('Digite a quantidade: '))
                self.showUsers()
                userId = int(input('Digite seu id de usuário: '))
                self._stock.updateItem('out', code, quantity, userId)
            case '0':
                pass
            case _:
                print('Opção inválida! Digite uma entrada válida.')
                self.showMoveOptions()
    
    def showSignUp(self):
        name = input('Digite o nome do usuário: ')
        self._usersManager.createUser(name)