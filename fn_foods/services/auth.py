from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        jwt_auth = JWTAuthentication()
        
        # Tenta pegar o usuário do token
        user, _ = jwt_auth.authenticate(request)
        
        if user is None or not user.is_authenticated:
            raise AuthenticationFailed('Token inválido ou ausente')
        
        return user
