from pydantic import BaseModel, EmailStr, Field
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from typing import Optional
from django.http.response import HttpResponse
from .models import ItensPedido,Pedido


class UsuarioSchemaIn(BaseModel):
    id: Optional[int] = None 
    username: str
    email: EmailStr 
    password: str = Field(..., min_length=6)  

    class Config:
        from_attributes = True 

    @classmethod
    def validate_orm(cls, usuario: User):
        return cls.model_validate(usuario)

    def create_user(self) -> User:
    
        if User.objects.filter(email=self.email).exists():
            return HttpResponse("Email já existente", status=400)
        
        if User.objects.filter(username=self.username).exists():
            return HttpResponse("Username já existente", status=400)
        
        senha_hash = make_password(self.password)
        
        return User.objects.create(username=self.username, email=self.email, password=senha_hash)

class UsuarioSchemaOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool 
    is_staff: bool 
    date_joined: str 

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, usuario: User):
        return cls(
            id=usuario.id,
            username=usuario.username,
            email=usuario.email,
            is_active=usuario.is_active,
            is_staff=usuario.is_staff,
            date_joined=usuario.date_joined.isoformat(),  
        )

class PedidoSchema(BaseModel):
    id: int
    total: float
    status: str
    data_pedido: str
    usuario_id: int

    class Config:
        from_attributes = True  # Permite que o modelo converta instâncias ORM

class UsuarioSchemaUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)  

    class Config:
        from_attributes = True

    def update_user(self, usuario: User) -> User:
        if self.username:
            usuario.username = self.username
        if self.email:
            usuario.email = self.email
        if self.password:
            usuario.password = make_password(self.password)
        usuario.save()

class LoginSchema(BaseModel):
    username: str
    password: str = Field(..., min_length=6) 
      

class SignupSchema(BaseModel):
    username: str
    password: str = Field(..., min_length=6)
    email:str    

class ItensPedidoSchemaIn(BaseModel):
    pedido_id: int
    nome: str
    descricao: Optional[str] = None
    quantidade: int = Field(..., gt=0)  # Quantidade deve ser maior que 0
    preco: float = Field(..., gt=0)   # Preço deve ser maior que 0
    categoria: str = Field(..., pattern="^(bebida|sobremesa|salada|acompanhamento)$")

    class Config:
        from_attributes = True

    def create_item_pedido(self) -> ItensPedido:
        # Buscar a instância do Pedido pelo ID
        try:
            pedido = Pedido.objects.get(id=self.pedido_id)  # Obtém o pedido pela chave estrangeira
        except Pedido.DoesNotExist:
            raise HttpError(status_code=404, message="Pedido não encontrado")

        # Criar o item de pedido com a instância do Pedido
        return ItensPedido.objects.create(
            pedido_id=pedido,  # Atribuir a instância de Pedido
            nome=self.nome,
            descricao=self.descricao,
            quantidade=self.quantidade,
            preco=self.preco,
            categoria=self.categoria
        )


class ItensPedidoSchemaOut(BaseModel):
    id: int
    pedido_id: int
    nome: str
    descricao: Optional[str]
    quantidade: int
    preco: float
    categoria: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, item: ItensPedido):
        return cls(
            id=item.id,
            pedido_id=item.pedido_id.id,
            nome=item.nome,
            descricao=item.descricao,
            quantidade=item.quantidade,
            preco=item.preco,
            categoria=item.categoria,
        )

class ItensPedidoSchemaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    quantidade: Optional[int] = Field(None, gt=0)
    preco: Optional[float] = Field(None, gt=0)
    categoria: Optional[str] = Field(None, pattern="^(bebida|sobremesa|salada|acompanhamento)$")

    class Config:
        from_attributes = True

    def update_item_pedido(self, item: ItensPedido) -> ItensPedido:
        for attr, value in self.dict(exclude_unset=True).items():
            setattr(item, attr, value)
        item.save()
        return item
    
class PedidoSchemaIn(BaseModel):
    total: float
    status: str = Field(default="pendente")
    usuario_id: int

    class Config:
        from_attributes = True

    def create_pedido(self) -> Pedido:
        try:
            # Buscando a instância do usuário correspondente ao ID fornecido
            usuario = User.objects.get(id=self.usuario_id)
        except User.DoesNotExist:
            raise HttpResponse(f"Usuário com id {self.usuario_id} não encontrado", status=400)
        
        # Agora criamos o pedido com a instância do usuário
        return Pedido.objects.create(
            total=self.total,
            status=self.status,
            usuario_id=usuario  # Atribuindo a instância de usuário
        )



class PedidoSchemaOut(BaseModel):
    id: int
    total: float
    status: str
    data_pedido: str
    usuario_id: int

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, pedido: Pedido):
        return cls(
            id=pedido.id,
            total=pedido.total,
            status=pedido.status,
            data_pedido=pedido.data_pedido.isoformat(),  # ISO 8601 format
            usuario_id=pedido.usuario_id.id
        )


class PedidoSchemaUpdate(BaseModel):
    total: Optional[float] = None
    status: Optional[str] = None
    usuario_id: Optional[int] = None

    class Config:
        from_attributes = True

    def update_pedido(self, pedido: Pedido) -> Pedido:
        if self.total:
            pedido.total = self.total
        if self.status:
            pedido.status = self.status
        if self.usuario_id:
            pedido.usuario_id = self.usuario_id
        pedido.save()
        return pedido