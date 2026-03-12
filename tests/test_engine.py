import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.engine import AuroraEngine

class TestAuroraEngine(unittest.TestCase):
    def test_process_data(self):
        engine = AuroraEngine()
        test_data = "hello world"
        expected_result = "Dados processados: HELLO WORLD"
        self.assertEqual(engine.process_data(test_data), expected_result)

if __name__ == '__main__':
    unittest.main()
