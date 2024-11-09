from ninja import Router
from ninja.errors import HttpError
from ..models import ItensPedido
from ..schemas import ItensPedidoSchemaIn, ItensPedidoSchemaOut, ItensPedidoSchemaUpdate

itens_pedido_router = Router()

@itens_pedido_router.post("/", response=ItensPedidoSchemaOut)
def criar_item_pedido(request, dados: ItensPedidoSchemaIn):
    item = dados.create_item_pedido()
    return ItensPedidoSchemaOut.from_orm(item)

@itens_pedido_router.get("/", response=list[ItensPedidoSchemaOut])
def listar_itens_pedido(request):
    itens = ItensPedido.objects.all()
    return [ItensPedidoSchemaOut.from_orm(item) for item in itens]

@itens_pedido_router.get("/{item_id}/", response=ItensPedidoSchemaOut)
def obter_item_pedido(request, item_id: int):
    try:
        item = ItensPedido.objects.get(id=item_id)
        return ItensPedidoSchemaOut.from_orm(item)
    except ItensPedido.DoesNotExist:
        raise HttpError(status_code=404, message="Item não encontrado")

@itens_pedido_router.put("/{item_id}/", response=ItensPedidoSchemaOut)
def atualizar_item_pedido(request, item_id: int, dados: ItensPedidoSchemaUpdate):
    try:
        item = ItensPedido.objects.get(id=item_id)
        item_atualizado = dados.update_item_pedido(item)
        return ItensPedidoSchemaOut.from_orm(item_atualizado)
    except ItensPedido.DoesNotExist:
        raise HttpError(status_code=404, message="Item não encontrado")

@itens_pedido_router.delete("/{item_id}/")
def deletar_item_pedido(request, item_id: int):
    try:
        item = ItensPedido.objects.get(id=item_id)
        item.delete()
        return {"success": True}
    except ItensPedido.DoesNotExist:
        raise HttpError(status_code=404, message="Item não encontrado")
