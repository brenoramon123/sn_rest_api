from ninja import Router
from django.http import HttpResponse
from ..models import Pedido
from ..schemas import PedidoSchemaIn, PedidoSchemaOut,PedidoSchemaUpdate

pedido_router = Router()

@pedido_router.post("/", response=PedidoSchemaOut)
def criar_pedido(request, dados: PedidoSchemaIn):
    try:
        pedido = dados.create_pedido()
        return PedidoSchemaOut.from_orm(pedido)
    except Exception as e:
        return HttpResponse(f"Erro ao criar pedido: {str(e)}", status=400)

@pedido_router.get("/", response=list[PedidoSchemaOut])
def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    return [PedidoSchemaOut.from_orm(pedido) for pedido in pedidos]

@pedido_router.get("/{pedido_id}", response=PedidoSchemaOut)
def detalhar_pedido(request, pedido_id: int):
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        return PedidoSchemaOut.from_orm(pedido)
    except Pedido.DoesNotExist:
        return HttpResponse(f"Pedido com id {pedido_id} não encontrado", status=404)

@pedido_router.put("/{pedido_id}", response=PedidoSchemaOut)
def atualizar_pedido(request, pedido_id: int, dados: PedidoSchemaUpdate):
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        updated_pedido = dados.update_pedido(pedido)
        return PedidoSchemaOut.from_orm(updated_pedido)
    except Pedido.DoesNotExist:
        return HttpResponse(f"Pedido com id {pedido_id} não encontrado", status=404)

@pedido_router.delete("/{pedido_id}", response={200: str, 404: str})
def deletar_pedido(request, pedido_id: int):
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        pedido.delete()
        return HttpResponse(f"Pedido {pedido_id} deletado com sucesso", status=200)
    except Pedido.DoesNotExist:
        return HttpResponse(f"Pedido com id {pedido_id} não encontrado", status=404)
