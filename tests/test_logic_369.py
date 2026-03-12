import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.logic_369 import Logic369

class TestLogic369(unittest.TestCase):
    def test_optimize(self):
        logic = Logic369()
        test_data = "sample data"
        # Since hash() can vary across Python runs, we'll test the format rather than exact value
        result = logic.optimize(test_data)
        self.assertTrue(result.startswith("Dados otimizados pela frequência 369: sample data -> "))
        self.assertTrue(result.endswith(str(hash(test_data) % 369)))

if __name__ == '__main__':
    unittest.main()
