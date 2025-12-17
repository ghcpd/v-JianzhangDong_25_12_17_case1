import unittest
from app.math_utils import factorial, is_prime
from app.data_processor import DataProcessor

class TestMain(unittest.TestCase):
    def test_factorial(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(5), 120)

    def test_is_prime(self):
        self.assertTrue(is_prime(2))
        self.assertFalse(is_prime(4))

    def test_data_processor(self):
        data = [1, 2, 3]
        processor = DataProcessor(data)
        normalized = processor.normalize()
        self.assertAlmostEqual(normalized[0], 0.0)
        self.assertAlmostEqual(normalized[-1], 1.0)

if __name__ == "__main__":
    unittest.main()
