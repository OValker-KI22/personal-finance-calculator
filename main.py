"""
Калькулятор личных финансов
"""


class FinanceCalculator:
    def __init__(self):
        """Инициализация калькулятора с пустыми списками операций"""
        self.incomes = []  # Доходы
        self.expenses = []  # Расходы
        self.categories = {
            'food': 0,
            'transport': 0,
            'entertainment': 0,
            'bills': 0,
            'shopping': 0,
            'health': 0,
            'education': 0,
            'other': 0
        }
#Проверка
    def add_income(self, amount: float, description: str = ""):
        """Добавление дохода"""
        if amount <= 0:
            raise ValueError("Сумма дохода должна быть положительной")

        income_record = {
            'amount': amount,
            'description': description,
            'date': self._get_current_date()
        }
        self.incomes.append(income_record)
        return income_record

    def add_expense(self, amount: float, category: str, description: str = ""):
        """Добавление расхода"""
        if amount <= 0:
            raise ValueError("Сумма расхода должна быть положительной")

        if category not in self.categories:
            raise ValueError(f"Категория '{category}' не поддерживается")

        expense_record = {
            'amount': amount,
            'category': category,
            'description': description,
            'date': self._get_current_date()
        }
        self.expenses.append(expense_record)
        self.categories[category] += amount
        return expense_record

    def get_total_income(self) -> float:
        """Получить общую сумму доходов"""
        return sum(item['amount'] for item in self.incomes)

    def get_total_expenses(self) -> float:
        """Получить общую сумму расходов"""
        return sum(item['amount'] for item in self.expenses)

    def get_balance(self) -> float:
        """Получить баланс (доходы - расходы)"""
        return self.get_total_income() - self.get_total_expenses()

    def get_expenses_by_category(self) -> dict:
        """Получить расходы по категориям"""
        return self.categories.copy()

    def get_top_expense_category(self) -> tuple:
        """Получить категорию с наибольшими расходами"""
        if not self.categories:
            return None, 0

        max_category = max(self.categories, key=self.categories.get)
        return max_category, self.categories[max_category]

    def get_monthly_summary(self, month: int, year: int) -> dict:
        """Получить сводку за конкретный месяц"""
        # В реальном приложении здесь была бы фильтрация по дате
        return {
            'month': month,
            'year': year,
            'total_income': self.get_total_income(),
            'total_expenses': self.get_total_expenses(),
            'balance': self.get_balance(),
            'expenses_by_category': self.get_expenses_by_category()
        }

    def reset(self):
        """Сбросить все данные"""
        self.incomes.clear()
        self.expenses.clear()
        for category in self.categories:
            self.categories[category] = 0

    def _get_current_date(self):
        """Получить текущую дату (упрощённая версия)"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def export_to_csv(self, filename: str = "finance_report.csv"):
        """Экспорт данных в CSV файл"""
        import csv

        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Заголовок
            writer.writerow(['Type', 'Amount', 'Category', 'Description', 'Date'])

            # Доходы
            for income in self.incomes:
                writer.writerow([
                    'INCOME',
                    income['amount'],
                    '',
                    income['description'],
                    income['date']
                ])

            # Расходы
            for expense in self.expenses:
                writer.writerow([
                    'EXPENSE',
                    expense['amount'],
                    expense['category'],
                    expense['description'],
                    expense['date']
                ])


# Пример использования калькулятора
def main():
    calculator = FinanceCalculator()

    # Добавляем доходы
    calculator.add_income(50000, "Зарплата")
    calculator.add_income(15000, "Фриланс")

    # Добавляем расходы
    calculator.add_expense(15000, "food", "Продукты на месяц")
    calculator.add_expense(5000, "transport", "Бензин")
    calculator.add_expense(8000, "bills", "Коммунальные услуги")
    calculator.add_expense(3000, "entertainment", "Кино")

    # Выводим результаты
    print("=" * 50)
    print("ФИНАНСОВЫЙ ОТЧЕТ")
    print("=" * 50)
    print(f"Общий доход: {calculator.get_total_income():.2f} руб.")
    print(f"Общие расходы: {calculator.get_total_expenses():.2f} руб.")
    print(f"Баланс: {calculator.get_balance():.2f} руб.")
    print("\nРасходы по категориям:")

    for category, amount in calculator.get_expenses_by_category().items():
        if amount > 0:
            print(f"  - {category}: {amount:.2f} руб.")

    top_category, top_amount = calculator.get_top_expense_category()
    if top_amount > 0:
        print(f"\nСамая затратная категория: {top_category} ({top_amount:.2f} руб.)")

    # Экспорт в CSV
    calculator.export_to_csv()
    print(f"\nОтчёт сохранён в finance_report.csv")


if __name__ == "__main__":
    main()