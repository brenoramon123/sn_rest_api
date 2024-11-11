# Usando a imagem oficial do Python como base
FROM python:3.11-slim

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Copiando o arquivo entrypoint.sh para o container
COPY entrypoint.sh /app/entrypoint.sh

# Tornar o script entrypoint.sh executável
RUN chmod +x /app/entrypoint.sh

# Instalar dependências do sistema e ferramentas necessárias
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    libmariadb-dev \
    wget \
    gcc \
    default-libmysqlclient-dev && \
    # Instalar dockerize
    wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && \
    tar -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && \
    mv dockerize /usr/local/bin/ && \
    rm -rf /var/lib/apt/lists/* && \
    rm dockerize-linux-amd64-v0.6.1.tar.gz

# Copiando o arquivo requirements.txt para o container
COPY requirements.txt .

# Instalando as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o código do projeto e o script wait-for-it.sh para dentro do container
COPY . .

# Tornar o script wait-for-it.sh executável
RUN chmod +x /app/wait-for-it.sh

# Expondo a porta 8000 para acesso à aplicação Django
EXPOSE 8000

# Comando para rodar o script wait-for-it e depois iniciar o Django
CMD ["/app/entrypoint.sh"]
