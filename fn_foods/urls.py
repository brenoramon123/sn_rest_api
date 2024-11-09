from django.urls import path
from ninja import NinjaAPI
from .api.pedido_router import pedido_router
from .api.auth_router import auth_router
from .api.usuario_router import usuario_router
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


api = NinjaAPI()

api.add_router("/auth/", auth_router)
api.add_router("/pedidos/", pedido_router)
api.add_router("/usuarios/", usuario_router)


urlpatterns = [
    path("api/", api.urls),  
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
