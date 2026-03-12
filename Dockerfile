# Use uma imagem base Python oficial
FROM python:3.9-slim-buster

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o arquivo de requisitos e instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para o diretório de trabalho
COPY . .

# Comando para executar a aplicação (exemplo, pode ser ajustado conforme a necessidade)
# Por exemplo, para rodar o engine.py
CMD ["python", "core/engine.py"]

# Exemplo de como construir e rodar:
# docker build -t aurora-sovereign-intelligence .
# docker run aurora-sovereign-intelligence
