import os
import tempfile
import unittest

import finance


class FinanceTest(unittest.TestCase):
    def setUp(self):
        handle, self.path = tempfile.mkstemp(suffix=".csv")
        os.close(handle)
        os.remove(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_add_and_load(self):
        finance.add_transaction(finance.INCOME, "Зарплата", 50000, day="2026-11-01", path=self.path)
        rows = finance.load_transactions(self.path)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["amount"], 50000.0)

    def test_balance(self):
        finance.add_transaction(finance.INCOME, "Зарплата", 50000, day="2026-11-01", path=self.path)
        finance.add_transaction(finance.EXPENSE, "Продукты", 12000, day="2026-11-03", path=self.path)
        rows = finance.load_transactions(self.path)
        self.assertEqual(finance.balance(rows), (50000.0, 12000.0, 38000.0))

    def test_wrong_amount(self):
        with self.assertRaises(ValueError):
            finance.add_transaction(finance.EXPENSE, "Кафе", -100, path=self.path)

    def test_report_by_category(self):
        for category, amount in [("Продукты", 6000), ("Транспорт", 2000), ("Продукты", 2000)]:
            finance.add_transaction(finance.EXPENSE, category, amount, day="2026-11-05", path=self.path)
        finance.add_transaction(finance.EXPENSE, "Кафе", 500, day="2026-10-20", path=self.path)
        rows = finance.filter_by_month(finance.load_transactions(self.path), "2026-11")
        report = finance.expenses_by_category(rows)
        self.assertEqual(report[0], ("Продукты", 8000.0, 80.0))
        self.assertEqual(report[1], ("Транспорт", 2000.0, 20.0))


if __name__ == "__main__":
    unittest.main()