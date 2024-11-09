﻿# Sistema de Pedidos - API REST com Django Ninja

Este projeto é uma API RESTful desenvolvida com Django e Django Ninja para gerenciar pedidos e itens de pedidos. O sistema é integrado com um banco de dados MySQL e utiliza JWT (JSON Web Tokens) para autenticação.

## Tecnologias Utilizadas

- **Django**: Framework para desenvolvimento web.
- **Django Ninja**: Framework para criação de APIs rápidas e eficientes com Django.
- **MySQL**: Banco de dados relacional para armazenar as informações.
- **JWT (JSON Web Tokens)**: Usado para autenticação e autorização segura de usuários.
- **Python 3.13.0**: Versão.

## Funcionalidades

- **Criação de Pedidos**: Permite a criação de pedidos por usuários autenticados.
- **Cadastro de Itens de Pedido**: Adição de itens (bebidas, sobremesas, etc.) a um pedido.
- **Listagem de Pedidos**: Listagem de pedidos realizados pelo usuário.
- **Atualização de Status do Pedido**: Atualização do status do pedido (Pendente, Em Preparação, A Caminho, Entregue).

- **Autenticação com Simple JWT**: Protege as rotas com autenticação JWT.
## Documentação das rotas com Swagger:
http://localhost:8000/api/docs

## Estrutura dos Models

### Pedido

O modelo `Pedido` representa um pedido feito por um usuário. Ele contém as seguintes informações:

- **total**: Valor total do pedido.
- **usuario_id**: Relacionamento com o modelo `User` do Django (usuário que fez o pedido).
- **status**: Status atual do pedido. Pode ser um dos seguintes: `pendente`, `em_preparacao`, `a_caminho`, `entregue`.
- **data_pedido**: Data e hora em que o pedido foi feito.

```python
class Pedido(models.Model):
    ENUM_STATUS = [
        ('pendente', 'Pendente'),
        ('em_preparacao', 'Em Preparação'),
        ('a_caminho', 'A Caminho'),
        ('entregue', 'Entregue'),
    ]

    total = models.DecimalField(max_digits=12, decimal_places=2)
    usuario_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ENUM_STATUS, default='pendente')
    data_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.status}"
```

### ItensPedido

O modelo `ItensPedido` representa os itens associados a um pedido. Ele contém as seguintes informações:

- **pedido_id**: Relacionamento com o modelo `Pedido`.
- **nome**: Nome do item.
- **descricao**: Descrição do item.
- **quantidade**: Quantidade do item no pedido.
- **preco**: Preço do item.
- **categoria**: Categoria do item (bebida, sobremesa, salada, acompanhamento).

```python
class ItensPedido(models.Model):
    ENUM_CATEGORIA = [
        ('bebida', 'Bebida'),
        ('sobremesa', 'Sobremesa'),
        ('salada', 'Salada'),
        ('acompanhamento', 'Acompanhamento'),
    ]
    pedido_id = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    nome = models.CharField(max_length=90)
    descricao = models.CharField(max_length=130)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=ENUM_CATEGORIA, default='bebida')

    def __str__(self):
        return f"{self.quantidade} x {self.nome} - {self.preco} cada"
```

## Como Executar o Projeto

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Instalar Dependências

Primeiro, crie um ambiente virtual e ative-o:

```bash
python -m venv venv
source venv/bin/activate   # No Windows: venv\Scripts\activate
```

Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

### 3. Configurar o Banco de Dados MySQL

Certifique-se de que o MySQL está instalado e configurado no seu sistema. Crie um banco de dados para o projeto:

```bash
mysql -u root -p
CREATE DATABASE sn_foods;
```

No arquivo `settings.py`, configure o banco de dados MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sn_foods',
        'USER': 'root',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. Rodar as Migrações

Após configurar o banco de dados, rode as migrações para criar as tabelas no banco de dados:

```bash
python manage.py migrate
```

### 5. Criar Superusuário (opcional)

Se quiser acessar o painel administrativo do Django, crie um superusuário:

```bash
python manage.py createsuperuser
```

### 6. Rodar o Servidor

Agora você pode rodar o servidor localmente:

```bash
python manage.py runserver
```

A API estará disponível em `http://127.0.0.1:8000/`.

## Autenticação com JWT

### 1. Login

Para obter um token JWT, faça uma requisição `POST` para o endpoint de criação de usuario com as credenciais do usuário:

```http
POST http://127.0.0.1:8000/api/signup/
Content-Type: application/json

{
    "username": "exemplo",
    "email": "exemplo@exemplo.com",
    "password": "exemplo"
}

```

e logo após faça uma requisição para obter seu jwt token
```http
POST http://127.0.0.1:8000/api/login/
Content-Type: application/json

{
    username": "exemplo",
	"password": "exemplo"
	
}


```

A resposta será um token JWT que você pode usar para autenticar suas requisições.

### 2. Autorização nas Rotas

Adicione o token JWT no cabeçalho de suas requisições para acessar rotas protegidas:

```http
Authorization: Bearer seu_token_jwt
```



