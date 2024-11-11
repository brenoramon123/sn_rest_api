from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from ...models import Pedido, ItensPedido
import random

class Command(BaseCommand):
    help = "Popular banco de dados com dados de pedidos e itens"

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        usuarios = []
        for _ in range(5): 
            usuario = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password()
            )
            usuarios.append(usuario)
        
        pedidos = []
        for _ in range(10): 
            usuario = random.choice(usuarios)
            pedido = Pedido.objects.create(
                total=random.uniform(50, 500),  
                usuario_id=usuario,
                status=random.choice(['pendente', 'em_preparacao', 'a_caminho', 'entregue']),
                data_pedido=fake.date_this_year()
            )
            pedidos.append(pedido)

            for _ in range(random.randint(1, 5)): 
                ItensPedido.objects.create(
                    pedido_id=pedido,
                    nome=fake.word(),
                    descricao=fake.sentence(),
                    quantidade=random.randint(1, 10), 
                    preco=random.uniform(5, 100),  
                    categoria=random.choice(['bebida', 'sobremesa', 'salada', 'acompanhamento'])
                )

        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))
