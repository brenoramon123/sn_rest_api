#!/bin/bash
# Espera o banco de dados estar disponível
echo "Esperando o banco de dados..."
/app/wait-for-it.sh db:3306 --timeout=30 --strict -- echo "Banco de dados disponível!"

echo "Populando dados..."
python /app/manage.py popular_dados  

echo "Executando migrações..."
python manage.py migrate --noinput

# Inicia o servidor
echo "Iniciando servidor..."
python manage.py runserver 0.0.0.0:8000
