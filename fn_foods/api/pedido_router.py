from ninja import Router
from ..models import Pedido
from ..schemas import PedidoSchema

pedido_router = Router()

@pedido_router.get("/", response=list[PedidoSchema])
def listar_pedidos(request):
    return Pedido.objects.all()
