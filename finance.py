"""Учет личных финансов: хранение операций и расчеты."""

import csv
import os
from datetime import date

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transactions.csv")
FIELDS = ["date", "type", "category", "amount", "comment"]
INCOME = "доход"
EXPENSE = "расход"


def load_transactions(path=DATA_FILE):
    """Читает все операции из CSV-файла."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    for row in rows:
        row["amount"] = float(row["amount"])
    return rows


def add_transaction(kind, category, amount, comment="", day=None, path=DATA_FILE):
    """Проверяет данные и дописывает одну операцию в CSV-файл."""
    if kind not in (INCOME, EXPENSE):
        raise ValueError("тип операции должен быть «доход» или «расход»")
    if amount <= 0:
        raise ValueError("сумма должна быть больше нуля")
    if not category.strip():
        raise ValueError("категория не может быть пустой")
    day = day or date.today().isoformat()
    is_new_file = not os.path.exists(path)
    with open(path, "a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if is_new_file:
            writer.writeheader()
        writer.writerow({
            "date": day,
            "type": kind,
            "category": category.strip(),
            "amount": f"{amount:.2f}",
            "comment": comment.strip(),
        })


def balance(transactions):
    """Возвращает сумму доходов, сумму расходов и остаток."""
    income = sum(t["amount"] for t in transactions if t["type"] == INCOME)
    expense = sum(t["amount"] for t in transactions if t["type"] == EXPENSE)
    return income, expense, income - expense