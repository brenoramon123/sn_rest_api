from django.db import models
from django.contrib.auth.models import User

class Pedido(models.Model):
    ENUM_STATUS = [
        ('pendente', 'Pendente'),
        ('em_preparacao', 'Em Preparação'),
        ('a_caminho', 'A Caminho'),
        ('entregue', 'Entregue'),
    ]

    total = models.DecimalField(max_digits=12, decimal_places=2)
    usuario_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ENUM_STATUS, default='pendente')
    data_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.status}"

class ItensPedido(models.Model):
    ENUM_CATEGORIA = [
        ('bebida', 'Bebida'),
        ('sobremesa', 'Sobremesa'),
        ('salada', 'Salada'),
        ('acompanhamento', 'Acompanhamento'),
    ]
    pedido_id = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    nome = models.CharField(max_length=90)
    descricao = models.CharField(max_length=130)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=ENUM_CATEGORIA, default='bebida')

    def __str__(self):
        return f"{self.quantidade} x {self.nome} - {self.preco} cada"
