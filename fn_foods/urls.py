from django.urls import path
from ninja import NinjaAPI
from .api.pedido_router import pedido_router
from .api.signup_router import signup_router
from .api.usuario_router import usuario_router
from .api.item_pedido_router import itens_pedido_router


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


api = NinjaAPI()

api.add_router("/signup/", signup_router)
api.add_router("/pedidos/", pedido_router)
api.add_router("/usuarios/", usuario_router)
api.add_router("/itens_pedido/", itens_pedido_router)



urlpatterns = [
    path("api/", api.urls),  
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
