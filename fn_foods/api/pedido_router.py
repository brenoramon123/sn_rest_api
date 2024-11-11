from ninja import Router
from django.http import HttpResponse
from ..models import Pedido
from ..schemas import PedidoSchemaIn, PedidoSchemaOut,PedidoSchemaUpdate,PedidoPaginatedResponseSchema
from typing import List
from django.core.paginator import Paginator
from datetime import datetime

pedido_router = Router()

@pedido_router.post("/", response=PedidoSchemaOut)
def criar_pedido(request, dados: PedidoSchemaIn):
    try:
        pedido = dados.create_pedido()
        return PedidoSchemaOut.from_orm(pedido)
    except Exception as e:
        return HttpResponse(f"Erro ao criar pedido: {str(e)}", status=400)

@pedido_router.get("/por_data/", response=list[PedidoSchemaOut])
def listar_pedidos_por_data(request, data_inicio: str = None, data_fim: str = None):
    #Exemplo http://127.0.0.1:8000/api/pedidos/por_data/?data_inicio=2024-11-10T00:00:00
    try:
        if data_inicio:
            data_inicio = datetime.fromisoformat(data_inicio)
        if data_fim:
            data_fim = datetime.fromisoformat(data_fim)
        
        if data_inicio and data_fim:
            pedidos = Pedido.objects.filter(data_pedido__range=[data_inicio, data_fim])
        elif data_inicio:
            pedidos = Pedido.objects.filter(data_pedido__gte=data_inicio)
        elif data_fim:
            pedidos = Pedido.objects.filter(data_pedido__lte=data_fim)
        else:
            pedidos = Pedido.objects.all()  
        return [PedidoSchemaOut.from_orm(pedido) for pedido in pedidos]
    
    except ValueError as e:
        return HttpResponse(f"Erro ao converter datas: {str(e)}", status=400)


@pedido_router.get("/paginado/", response=PedidoPaginatedResponseSchema)
def listar_pedido_paginado(request, page: int = 1, per_page: int = 10):
    itens = Pedido.objects.all()
    
    paginator = Paginator(itens, per_page)
    
    page_obj = paginator.get_page(page)
    
    itens_pagina = [PedidoSchemaOut.from_orm(item) for item in page_obj]
    
    response_data = PedidoPaginatedResponseSchema(
        items=itens_pagina,
        total_pages=paginator.num_pages,
        current_page=page_obj.number,
        has_next=page_obj.has_next(),
        has_previous=page_obj.has_previous()
    )
    
    return response_data

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
