from pydantic import BaseModel, EmailStr, Field
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from typing import Optional
from django.http.response import HttpResponse


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
