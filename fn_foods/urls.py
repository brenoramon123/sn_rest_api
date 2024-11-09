from django.urls import path
from ninja import NinjaAPI
from .api.pedido_router import pedido_router
from .api.usuario_router import usuario_router


api = NinjaAPI()

api.add_router("/pedidos/", pedido_router)
api.add_router("/usuarios/", usuario_router)

urlpatterns = [
    path("api/", api.urls),  
]
