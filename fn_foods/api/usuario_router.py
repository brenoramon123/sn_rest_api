from ninja import Router
from ..schemas import UsuarioSchema
from django.contrib.auth.models import User as Usuario


usuario_router = Router()

@usuario_router.get("/", response=list[UsuarioSchema])
def listar_usuarios(request):
    return Usuario.objects.all()

@usuario_router.post("/", response=UsuarioSchema)
def criar_usuario(request, usuario: UsuarioSchema):
    novo_usuario = Usuario.objects.create(**usuario.dict())
    return novo_usuario

@usuario_router.get("/{usuario_id}", response=UsuarioSchema)
def obter_usuario(request, usuario_id: int):
    return Usuario.objects.get(id=usuario_id)

@usuario_router.put("/{usuario_id}", response=UsuarioSchema)
def atualizar_usuario(request, usuario_id: int, dados: UsuarioSchema):
    usuario = Usuario.objects.get(id=usuario_id)
    for attr, value in dados.dict().items():
        setattr(usuario, attr, value)
    usuario.save()
    return usuario

@usuario_router.delete("/{usuario_id}")
def deletar_usuario(request, usuario_id: int):
    Usuario.objects.filter(id=usuario_id).delete()
    return {"sucesso": True}
