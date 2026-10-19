import tempfile
import unittest
from pathlib import Path
from expenses import add_expense, total_expenses

class ExpenseTests(unittest.TestCase):
    def test_persistence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "expenses.csv"
            self.assertEqual(total_expenses(path), 0)
            add_expense(path, "food", 3000)
            add_expense(path, "travel", 1500)
            self.assertEqual(total_expenses(path), 4500)

    def test_invalid_amount(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "expenses.csv"
            with self.assertRaises(ValueError):
                add_expense(path, "food", -1)
            self.assertFalse(path.exists())
