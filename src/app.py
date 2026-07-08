from src.exceptions import ItemException, StockException, UserException
from datetime import datetime
from src.stock import Stock
from src.usersManager import UsersManager
from src.entities.item import Item

class StockApp:
    LARGURA = 70

    def __init__(self):
        self._stock = Stock()
        self._usersManager = UsersManager()
        #inicia o sistema
        self.run()

    def printTitle(self, title: str):
        '''Sessão de título'''
        print()
        print('=' * self.LARGURA)
        print(title.center(self.LARGURA))
        print('=' * self.LARGURA)

    def printDivider(self):
        print('-' * self.LARGURA)

    def printSucess(self, message: str):
        print(f'\n[OK]: {message}\n')

    def printError(self, message: str):
        print(f'\n[ERRO]: {message}\n')       

    def printInfo(self, message: str):
        print(f'\n[AVISO]: {message}\n')     
    
    def run(self):
        '''Looping principal, interação com o usuário'''
        self.printTitle('Bem vindo ao sistema de controle de estoque!')
        while True:
            self.printTitle('SISTEMA DE CONTROLE DE ESTOQUE')
            print('1- Listar itens no estoque')
            print('2- Movimentar item do estoque')
            print('3- Listar movimentações recentes')
            print('4- Cadastrar usuário')
            print('5- Listar usuários')
            print('0- Encerrar')
            self.printDivider()
            option = input('Digite sua opção: ')
            self.printDivider()
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
                    #usuario escolheu sair do aplicativo
                    print('\nEncerrando... Até logo!\n')
                    break
                case _ :
                    #usuário digitou um opção inválida
                    self.printError('Opção inválida.')

    def showItems(self):
        '''Mostra a lista de itens no estoque'''
        #checka se existem item no estoque
        if not self._stock.hasItems:
            self.printInfo('Nenhum item cadastrado no estoque.')
            return
        self.printTitle('ITENS NO ESTOQUE')
        print(f'{"Código":<10} {"Nome":<32} {"Quantidade":>12}')
        self.printDivider()
        for item in self._stock.getItems():
            code = f'{item.code:04d}'
            print(f'{code:<10} {self.fit(item.name, 32):<32} {item.quantity:>12}')
        self.printDivider()

    def showUsers(self):
        '''Mostra a lista de usuários cadastrados no sistema'''
        #checka se existem usuários cadastrados no sistema
        if not self._usersManager.hasUsers:
            self.printInfo('Nenhum usuário cadastrado no sistema.')
            return
        self.printTitle('USUÁRIOS CADASTRADOS')
        print(f'{"Id":<8} {"Nome":<40}')
        self.printDivider()
        for user in self._usersManager.getUsers():
            userId = f'{user.id:04d}'
            print(f'{userId:<8} {self.fit(user.name, 40):<40}')
        self.printDivider()

    def showRecentMoves(self):
        '''Mostra as movimentações recentes no estoque'''
        transactions = self._stock.getTransactions()
        #checka se existem movimentações
        if not transactions:
            self.printInfo('Nenhuma movimentação registrada.')
            return
        self.printTitle('MOVIMENTAÇÕES RECENTES')
        print(f'{"Id":<6} {"Data":<12} {"Tipo":<9} {"Item":<22} {"Qtd":<5} {"Usuário":<15}')
        self.printDivider()
        for t in self._stock.getTransactions():
            tId = f'{t.id:04d}'
            print(f'{tId:<6} {t.date:<12} {self.translateType(t.type):<9} {t.itemName:<22} {t.quantity:<5} {t.userName:<15}')
        self.printDivider()

    def showMoveOptions(self):
        '''Mostra as opções de movimentação de um item no estoque e solicita opção do usuário'''
        print('1- Adicionar novo item')
        print('2- Adicionar item existente')
        print('3- Retirar item')
        print('0- Voltar')
        self.printDivider()
        option = input('Digite sua opção: ')
        self.printDivider()
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
                    #usuário digitou uma entrada inválida
                    self.printInfo('Opção inválida! Digite uma entrada válida.')
                    self.showMoveOptions()
        except (ItemException, StockException, UserException) as e:
            #sistema detectou algum problema ao tentar adicionar ou remover um item
            self.printError(str(e))

    def showCreateItem(self):
        '''Criação de um item. Solicita as informações necessárias para cadastrar um item no sistema'''
        #checka se existem usuários no sistema
        if not self._usersManager.hasUsers:
            self.printInfo('Nenhum usuário cadastrado no sistema.')
            return
        name = self.readNewItemName()
        initialQuantity = self.readPositiveInt('Digite a quantidade inicial inserida: ')
        date = self.readDate('Data de entrada (dd/mm/aaaa, Enter = hoje): ')
        userId = self.readUserId()
        item = Item(name, initialQuantity)
        self._stock.insertItem(item, userId, date)
        self.printSucess('Item cadastrado com sucesso!')

    def showAddItem(self):
        '''Adicionar um item existente. Solicita informações sobre a adição a ser realizada'''
        #checka se existem usuários cadastrados no sistema
        if not self._usersManager.hasUsers:
            self.printInfo('Nenhum usuário cadastrado no sistema.')
            return
        #checka se existem itens no estoque
        if not self._stock.hasItems:
            self.printInfo('Nenhum item cadastrado no estoque.')
            return
        self.showItems()
        while True:
            code = self.readInt('Digite o código do item: ')
            #checka se o item existe no estoque
            if self._stock.getItem(code) is not None:
                break
            self.printInfo('Item não encontrado no sistema. Digite um código válido.')
        quantity = self.readPositiveInt('Digite a quantidade: ')
        date = self.readDate('Data de entrada (dd/mm/aaaa, Enter = hoje): ')
        userId = self.readUserId()
        self._stock.updateItem('in', code, quantity, userId, date)
        self.printSucess('Entrada registrada com sucesso!')

    def showRmvItem(self):
        '''Remove um item do estoque. Solicita informações sobre a retirada a ser realizada'''
        #checka se existem usuários cadastrados no sistema
        if not self._usersManager.hasUsers:
            self.printInfo('Nenhum usuário cadastrado no sistema.')
            return
        #checka se existem itens no estoque
        if not self._stock.hasItems:
            self.printInfo('Nenhum item cadastrado no estoque.')
            return
        self.showItems()
        while True:
            code = self.readInt('Digite o código do item: ')
            #checka se o item existe no estoque
            if self._stock.getItem(code) is not None:
                break
            self.printInfo('Item não encontrado no sistema. Digite um código válido.')
        quantity = self.readPositiveInt('Digite a quantidade: ')
        date = datetime.now().strftime('%d/%m/%Y')
        userId = self.readUserId()
        self._stock.updateItem('out', code, quantity, userId, date)
        self.printSucess('Saída registrada com sucesso!')
    
    def showSignUp(self):
        '''Criação de usuário. Solicita as informações para criação de um novo usuário'''
        name = self.readNewUserName()
        self._usersManager.createUser(name)
        self.printSucess('Usuário cadastrado com sucesso!')

    def fit(self, text: str, width: int) -> str:
        '''Garante o tamanho do texto na tela, completando com "..." caso exceder o limite de largura'''
        return text if len(text) <= width else text[:width - 3] + '...'

    def translateType(self, type: str) -> str:
        '''Traduz os tipos de movimentação de estoque (Entrada/Saída)'''
        if type == 'in':
            return 'Entrada'
        else:
            return 'Saída'
        
    def readPositiveInt(self, message: str) -> int:
        '''Lê apenas números inteiros e positivos, sinalizando erros do usuário'''
        while True:
            value = self.readInt(message)
            if value > 0:
                return value
            self.printInfo('O valor digitado deve ser maior que zero.')

    def readInt(self, message: str) -> int:
        '''Lê apenas números inteiros, sinalizando erros do usuário'''
        while True:
            value = input(message).strip()
            try:
                #verifica conversão pra inteiro
                return int(value)
            except ValueError:
                self.printInfo('Valor inválido. Digite apenas números inteiros.')

    def readNewItemName(self) -> str:
        '''Garante o bloqueio de adição de itens com mesmo nome no estoque'''
        while True:
            name = self.readStr('Digite o nome do item: ')
            #checka se ja existe esse nome de item no estoque
            if self._stock.getItemByName(name) is None:
                return name
            self.printInfo(f'Já existe um item chamado "{name}". Escolha outro nome.')

    def readNewUserName(self) -> str:
        '''Garante o bloqueio de adição de usuários com mesmo nome no sistema'''
        while True:
            name = self.readStr('Digite o nome do usuário: ')
            #checka se ja existe esse nome de usuário no sistema
            if self._usersManager.getUserByName(name) is None:
                return name
            self.printInfo(f'Já existe um usuário chamado "{name}". Escolha outro nome.')

    def readStr(self, message: str) -> str:
        '''Garante que uma entrada do tipo "texto" não fique vazia'''
        while True:
            value = input(message).strip()
            if value:
                return value
            self.printInfo('O campo não pode ficar vazio')

    def readUserId(self) -> int:
        '''Garante que o usuário digitado existe'''
        self.showUsers()
        while True:
            userId = self.readInt('Digite seu id de usuário: ')
            #checka se o usuário está cadastrado no sistema
            if self._usersManager.getUser(userId) is not None:
                return userId
            self.printInfo('Usuário não encontrado! Informe um id da lista acima.')

    def readDate(self, message: str) -> str:
        '''Garante o formato da data e fornece data automática em caso de campo vazio'''
        while True:
            value = input(message).strip()
            #usuário apertou enter sem digitar a data
            if value == '':
                return datetime.now().strftime('%d/%m/%Y')
            try:
                #checka conversão para tipo data
                datetime.strptime(value, '%d/%m/%Y')
                return value
            except ValueError:
                self.printInfo('Data inválida! Use o formato dd/mm/aaaa.')