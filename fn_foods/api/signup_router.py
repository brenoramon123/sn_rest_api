from ninja import Router
from ..schemas import SignupSchema
from django.contrib.auth.models import User as Usuario
from ninja.errors import HttpError
from django.http import JsonResponse

signup_router = Router()

@signup_router.post("/", response=SignupSchema)
def criar_usuario(request, dados: SignupSchema):
    if Usuario.objects.filter(username=dados.username).exists():
        raise HttpError(400, "Username já existente")
    
    user = Usuario.objects.create_user(username=dados.username, email=dados.email, password=dados.password)
    return JsonResponse({"mensagem": "Usuário cadastrado com sucesso"})