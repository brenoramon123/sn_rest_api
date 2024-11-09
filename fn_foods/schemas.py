from ninja import Schema
from decimal import Decimal

class UsuarioSchema(Schema):
    id: int
    username: str
    email: str

class PedidoSchema(Schema):
    id: int
    total: Decimal
    status: str
    data_pedido: str
    usuario_id: int