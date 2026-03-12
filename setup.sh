#!/bin/bash

echo "Iniciando a configuração do ambiente Aurora Sovereign Intelligence..."

# Instalar dependências do Python
echo "Instalando dependências do Python..."
pip install -r requirements.txt

# Criar ambiente virtual (opcional, mas recomendado)
# echo "Criando ambiente virtual..."
# python -m venv venv
# source venv/bin/activate

echo "Configuração concluída. Para executar os exemplos, use:"
echo "python core/engine.py"
echo "python core/logic_369.py"
echo "python blockchain/aurora_chain.py"
echo "python agents/aninha_assistant.py"
