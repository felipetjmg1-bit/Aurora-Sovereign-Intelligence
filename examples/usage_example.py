# examples/usage_example.py

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.engine import AuroraEngine
from core.logic_369 import Logic369
from blockchain.aurora_chain import AuroraChain
from agents.aninha_assistant import AninhaAssistant

def run_aurora_example():
    print("\n--- Iniciando Exemplo de Uso do Aurora Sovereign Intelligence ---")

    # 1. Usando o Aurora Engine
    print("\n### Testando Aurora Engine ###")
    engine = AuroraEngine()
    processed_data = engine.process_data("dados brutos para o motor")
    print(f"Resultado do Engine: {processed_data}")

    # 2. Usando o Módulo Logic 369
    print("\n### Testando Logic 369 ###")
    logic_369 = Logic369()
    optimized_data = logic_369.optimize("informação para otimização")
    print(f"Resultado do Logic 369: {optimized_data}")

    # 3. Usando a Aurora Chain
    print("\n### Testando Aurora Chain ###")
    aurora_chain = AuroraChain()
    print(aurora_chain.connect_ton())
    integrated_drex = aurora_chain.integrate_drex("transacao_token_A")
    print(f"Resultado da Aurora Chain: {integrated_drex}")

    # 4. Usando a Aninha Assistant
    print("\n### Testando Aninha Assistant ###")
    aninha = AninhaAssistant()
    task_status = aninha.manage_task("preparar relatório mensal")
    print(f"Resultado da Aninha Assistant: {task_status}")

    print("\n--- Exemplo de Uso Concluído ---")

if __name__ == "__main__":
    run_aurora_example()
