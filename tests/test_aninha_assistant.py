import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.aninha_assistant import AninhaAssistant

class TestAninhaAssistant(unittest.TestCase):
    def test_manage_task(self):
        aninha = AninhaAssistant()
        test_task = "Agendar reunião"
        expected_result = "Tarefa 'Agendar reunião' gerenciada com sucesso pela Aninha Assistant."
        self.assertEqual(aninha.manage_task(test_task), expected_result)

if __name__ == '__main__':
    unittest.main()
