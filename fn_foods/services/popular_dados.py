import os
import django
from datetime import datetime
from ..models import Pedido

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seu_projeto.settings')
django.setup()

def popular_dados():
    pedidos = [
        Pedido(total=100.5, status='pendente', data_pedido=datetime(2024, 11, 11, 0, 13, 46), usuario_id=10),
        Pedido(total=150.0, status='concluido', data_pedido=datetime(2024, 11, 12, 1, 15, 30), usuario_id=11),
        Pedido(total=200.75, status='pendente', data_pedido=datetime(2024, 11, 13, 2, 17, 55), usuario_id=12),
    ]
    
    for pedido in pedidos:
        pedido.save()

    print("Dados populados com sucesso!")

if __name__ == '__main__':
    popular_dados()
