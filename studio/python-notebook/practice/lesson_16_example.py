# 17 / Test behaviour
import unittest

def total_amount(amounts):
    if any(x < 0 for x in amounts):
        raise ValueError("Negative amount")
    return sum(amounts)

class TotalTests(unittest.TestCase):
    def test_total(self):
        self.assertEqual(total_amount([2, 3]), 5)
    def test_empty(self):
        self.assertEqual(total_amount([]), 0)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            total_amount([-1])
