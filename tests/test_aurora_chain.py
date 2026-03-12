import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blockchain.aurora_chain import AuroraChain

class TestAuroraChain(unittest.TestCase):
    def test_connect_ton(self):
        chain = AuroraChain()
        self.assertEqual(chain.connect_ton(), "Conectado à rede TON.")

    def test_integrate_drex(self):
        chain = AuroraChain()
        test_data = "Transação de teste"
        self.assertEqual(chain.integrate_drex(test_data), "Dados integrados com DREX: Transação de teste_DREX")

if __name__ == '__main__':
    unittest.main()
