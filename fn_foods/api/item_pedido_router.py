from ninja import Router
from ninja.errors import HttpError
from ..models import ItensPedido
from ..schemas import ItensPedidoSchemaIn, ItensPedidoSchemaOut, ItensPedidoSchemaUpdate,ItensPedidoPaginatedResponseSchema
from typing import List
from django.core.paginator import Paginator

itens_pedido_router = Router()

@itens_pedido_router.post("/", response=ItensPedidoSchemaOut)
def criar_item_pedido(request, dados: ItensPedidoSchemaIn):
    try:
        item = dados.create_item_pedido()
        return ItensPedidoSchemaOut.from_orm(item)
    except HttpError as e:
        raise HttpError(status_code=404, message=f"Erro específico ao criar item: {e}")

@itens_pedido_router.get("/", response=list[ItensPedidoSchemaOut])
def listar_itens_pedido(request):
    itens = ItensPedido.objects.all() 
    return [ItensPedidoSchemaOut.from_orm(item) for item in itens]

@itens_pedido_router.get("/paginado/", response=ItensPedidoPaginatedResponseSchema)
def listar_itens_pedido_paginado(request, page: int = 1, per_page: int = 10):
    itens = ItensPedido.objects.all()
    
    paginator = Paginator(itens, per_page)
    
    page_obj = paginator.get_page(page)
    
    itens_pagina = [ItensPedidoSchemaOut.from_orm(item) for item in page_obj]
    
    response_data = ItensPedidoPaginatedResponseSchema(
        items=itens_pagina,
        total_pages=paginator.num_pages,
        current_page=page_obj.number,
        has_next=page_obj.has_next(),
        has_previous=page_obj.has_previous()
    )
    
    return response_data

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
