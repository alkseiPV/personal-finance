"""Консольное меню программы учета и анализа личных финансов."""

import finance


def ask_amount():
    """Запрашивает сумму, пока пользователь не введет положительное число."""
    while True:
        text = input("Сумма, руб.: ").replace(",", ".").strip()
        try:
            amount = float(text)
        except ValueError:
            print("Введите число, например 1500 или 249.90")
            continue
        if amount > 0:
            return amount
        print("Сумма должна быть больше нуля")


def add_operation(kind):
    category = input("Категория: ").strip()
    amount = ask_amount()
    comment = input("Комментарий (можно оставить пустым): ")
    try:
        finance.add_transaction(kind, category, amount, comment)
    except ValueError as error:
        print("Ошибка:", error)
        return
    print("Операция сохранена")


def show_operations():
    rows = finance.load_transactions()
    if not rows:
        print("Операций пока нет")
        return
    for row in rows:
        print(f"{row['date']}  {row['type']:<7} {row['category']:<15} {row['amount']:>10.2f}  {row['comment']}")


def show_balance():
    income, expense, rest = finance.balance(finance.load_transactions())
    print(f"Доходы:  {income:.2f} руб.")
    print(f"Расходы: {expense:.2f} руб.")
    print(f"Баланс:  {rest:.2f} руб.")


def show_report():
    month = input("Месяц в формате ГГГГ-ММ (пустой ввод означает текущий месяц): ").strip()
    if not month:
        month = finance.current_month()
    rows = finance.filter_by_month(finance.load_transactions(), month)
    income, expense, rest = finance.balance(rows)
    print(f"Отчет за {month}")
    print(f"Доходы: {income:.2f} руб., расходы: {expense:.2f} руб., остаток: {rest:.2f} руб.")
    report = finance.expenses_by_category(rows)
    if not report:
        print("Расходов за этот месяц нет")
        return
    print("Структура расходов:")
    for category, amount, share in report:
        print(f"  {category:<15} {amount:>10.2f} руб.  {share:5.1f} %")


MENU = {
    "1": ("Добавить доход", lambda: add_operation(finance.INCOME)),
    "2": ("Добавить расход", lambda: add_operation(finance.EXPENSE)),
    "3": ("Показать все операции", show_operations),
    "4": ("Показать баланс", show_balance),
    "5": ("Отчет по категориям расходов за месяц", show_report),
}


def main():
    print("Учет и анализ личных финансов")
    while True:
        print()
        for key, (title, _) in MENU.items():
            print(f"{key}. {title}")
        print("0. Выход")
        choice = input("Выберите пункт: ").strip()
        if choice == "0":
            break
        if choice in MENU:
            MENU[choice][1]()
        else:
            print("Такого пункта нет")


if __name__ == "__main__":
    main()