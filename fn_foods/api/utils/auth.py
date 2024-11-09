from ninja.security import django_auth
from ninja.errors import HttpError
class JWTAuth(django_auth.JWTAuth):
    def authenticate(self, request):
        if not request.user.is_authenticated:
            raise HttpError(401, "Token inválido ou ausente")
        return request.user