from ninja import Router
from ..schemas import UsuarioSchemaIn, UsuarioSchemaOut,SignupSchema, UsuarioSchemaUpdate,LoginSchema
from django.contrib.auth.models import User as Usuario

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ninja.errors import HttpError
from django.http.response import HttpResponse




usuario_router = Router()

@usuario_router.post("/signup", response=SignupSchema)
def criar_usuario(request, dados: SignupSchema):
    if Usuario.objects.filter(username=dados.username).exists():
        raise HttpError(400, "Username já existente")
    
    user = Usuario.objects.create_user(username=dados.username, email=dados.email, password=dados.password)
    return JsonResponse({"mensagem": "Usuário cadastrado com sucesso"})

@usuario_router.get("/", response=list[UsuarioSchemaIn])
def listar_usuarios(request):
    return Usuario.objects.all()

@usuario_router.get("/{usuario_id}", response=UsuarioSchemaIn)
def obter_usuario(request, usuario_id: int):
    return Usuario.objects.get(id=usuario_id)

@usuario_router.put("/{usuario_id}", response=UsuarioSchemaOut)
def atualizar_usuario(request, usuario_id: int, dados: UsuarioSchemaUpdate):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        raise HttpError(status_code=404, message="Usuário não encontrado")

    if usuario.id != request.user.id:
        raise HttpError(status_code=403, message="Você não tem permissão para editar este usuário.")
    
    for attr, value in dados.model_dump().items():
        if attr == "password" and value: 
            value = make_password(value)
        setattr(usuario, attr, value)
    
    usuario.save()

    return UsuarioSchemaOut.from_orm(usuario)

@usuario_router.delete("/{usuario_id}")
def deletar_usuario(request, usuario_id: int):
    Usuario.objects.filter(id=usuario_id).delete()
    return {"sucesso": True}
