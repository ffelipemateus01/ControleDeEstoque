# 📦 Controle de Estoque

Sistema de controle de estoque via terminal, desenvolvido em **Python puro** com persistência em **SQLite** — sem nenhuma dependência externa.

---

## ✨ Funcionalidades

- **Listagem de itens** — visualize todos os itens do estoque com código, nome e quantidade em uma tabela formatada.
- **Movimentação de estoque**
  - ➕ Cadastro de novos itens com quantidade inicial e data de entrada;
  - 📥 Entrada de itens já existentes;
  - 📤 Saída de itens, com bloqueio automático quando a quantidade em estoque é insuficiente.
- **Histórico de movimentações** — todas as entradas e saídas ficam registradas com data, item, quantidade e usuário responsável, listadas da mais recente para a mais antiga.
- **Gestão de usuários** — cadastro e listagem de usuários; toda movimentação é vinculada a um usuário do sistema.
- **Validações robustas de entrada**
  - Quantidades apenas inteiras e positivas;
  - Datas no formato `dd/mm/aaaa` (Enter usa a data de hoje automaticamente);
  - Bloqueio de itens e usuários com nomes duplicados;
  - Campos de texto não podem ficar vazios.
- **Persistência automática** — os dados são salvos em um banco SQLite local (`stockcontrol`), criado automaticamente na primeira execução.

## 🚀 Como executar

### Pré-requisitos

- [Python 3.10 ou superior]

Nenhuma biblioteca externa é necessária — apenas a biblioteca padrão do Python.

### Passo a passo

```bash
# Clone o repositório
git clone https://github.com/ffelipemateus01/ControleDeEstoque.git

# Entre na pasta do projeto
cd ControleDeEstoque

# Execute o sistema
python main.py
```

> 💡 Na primeira execução, o banco de dados `stockcontrol` será criado automaticamente na raiz do projeto. Cadastre um usuário (opção 4) antes de movimentar itens — toda movimentação exige um usuário responsável.

## 🗂️ Estrutura do projeto

```
ControleDeEstoque/
├── main.py                     # Ponto de entrada do aplicativo
└── src/
    ├── app.py                  # Interface CLI: menus, leitura e validação de entradas
    ├── stock.py                # Regras de negócio do estoque
    ├── usersManager.py         # Regras de negócio dos usuários
    ├── database.py             # Camada de acesso ao SQLite (queries e transações)
    ├── constants.py            # Constantes do sistema (nome do banco de dados)
    ├── exceptions.py           # Exceções personalizadas (Item, Stock e User)
    ├── util.py                 # Conversão dos dados do banco em entidades
    └── entities/
        ├── item.py             # Entidade Item
        ├── user.py             # Entidade User
        └── transaction.py      # Entidade Transaction (movimentação)
```

## 👨‍💻 Autor

Feito por [Felipe Mateus](https://github.com/ffelipemateus01).
