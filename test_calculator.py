import pytest
import os
from main import FinanceCalculator


class TestFinanceCalculator:
    def setup_method(self):
        """Инициализация перед каждым тестом"""
        self.calc = FinanceCalculator()

    def test_initial_state(self):
        """Тест начального состояния калькулятора"""
        assert self.calc.get_total_income() == 0
        assert self.calc.get_total_expenses() == 0
        assert self.calc.get_balance() == 0

    def test_add_income_positive(self):
        """Тест добавления дохода с положительной суммой"""
        income = self.calc.add_income(10000, "Зарплата")
        assert income['amount'] == 10000
        assert income['description'] == "Зарплата"
        assert self.calc.get_total_income() == 10000

    def test_add_income_negative_amount(self):
        """Тест добавления дохода с отрицательной суммой"""
        with pytest.raises(ValueError, match="Сумма дохода должна быть положительной"):
            self.calc.add_income(-1000, "Неверная сумма")

    def test_add_expense_valid_category(self):
        """Тест добавления расхода с валидной категорией"""
        expense = self.calc.add_expense(5000, "food", "Продукты")
        assert expense['amount'] == 5000
        assert expense['category'] == "food"
        assert self.calc.get_total_expenses() == 5000
        assert self.calc.get_expenses_by_category()['food'] == 5000

    def test_add_expense_invalid_category(self):
        """Тест добавления расхода с невалидной категорией"""
        with pytest.raises(ValueError, match="Категория 'invalid_category' не поддерживается"):
            self.calc.add_expense(1000, "invalid_category", "Неизвестная категория")

    def test_balance_calculation(self):
        """Тест расчёта баланса"""
        self.calc.add_income(50000, "Доход")
        self.calc.add_expense(30000, "bills", "Счета")

        assert self.calc.get_total_income() == 50000
        assert self.calc.get_total_expenses() == 30000
        assert self.calc.get_balance() == 20000

    def test_top_expense_category(self):
        """Тест определения самой затратной категории"""
        self.calc.add_expense(10000, "food", "Еда")
        self.calc.add_expense(5000, "transport", "Транспорт")
        self.calc.add_expense(15000, "food", "Еда ещё")

        top_category, top_amount = self.calc.get_top_expense_category()
        assert top_category == "food"
        assert top_amount == 25000

    def test_reset_function(self):
        """Тест сброса данных"""
        self.calc.add_income(10000, "Тест")
        self.calc.add_expense(5000, "food", "Тест")

        # Проверяем, что данные добавлены
        assert self.calc.get_total_income() > 0
        assert self.calc.get_total_expenses() > 0

        # Сбрасываем
        self.calc.reset()

        # Проверяем, что данные сброшены
        assert self.calc.get_total_income() == 0
        assert self.calc.get_total_expenses() == 0

        # Проверяем сброс категорий
        for amount in self.calc.get_expenses_by_category().values():
            assert amount == 0

    def test_monthly_summary(self):
        """Тест генерации месячного отчёта"""
        self.calc.add_income(50000, "Зарплата")
        self.calc.add_expense(15000, "food", "Еда")

        summary = self.calc.get_monthly_summary(11, 2024)

        assert summary['total_income'] == 50000
        assert summary['total_expenses'] == 15000
        assert summary['balance'] == 35000
        assert 'expenses_by_category' in summary

    def test_export_to_csv(self):
        """Тест экспорта в CSV"""
        # Добавляем тестовые данные
        self.calc.add_income(10000, "Тестовый доход")
        self.calc.add_expense(5000, "food", "Тестовые расходы")

        # Экспортируем
        filename = "test_report.csv"
        self.calc.export_to_csv(filename)

        # Проверяем, что файл создан
        assert os.path.exists(filename)

        # Проверяем содержимое файла
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            assert "INCOME" in content
            assert "EXPENSE" in content
            assert "food" in content

        # Удаляем тестовый файл
        os.remove(filename)

    def test_consecutive_operations(self):
        """Тест последовательных операций"""
        # Множественные операции
        for i in range(5):
            self.calc.add_income(1000 * (i + 1), f"Доход {i + 1}")

        assert self.calc.get_total_income() == 15000  # 1000+2000+3000+4000+5000

        # Множественные расходы
        categories = ["food", "transport", "bills"]
        for i, category in enumerate(categories):
            self.calc.add_expense(2000 * (i + 1), category, f"Расход {i + 1}")

        assert self.calc.get_total_expenses() == 12000  # 2000+4000+6000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])