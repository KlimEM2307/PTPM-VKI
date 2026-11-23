import unittest
from unittest.mock import MagicMock, patch

from src.controller import Controller
from src.database import TriangleDatabase
from src.notifier import Notifier, ConsoleNotifier
from src.triangle_calculator import TriangleCalculator, calculate_coords
from src.user_interface import UserInterface, ConsoleUserInterface


# ---------- Юнит-тесты класса вычислений ----------

class TestTriangleCalculator(unittest.TestCase):

    def test_equilateral(self):
        t_type, _, err = TriangleCalculator.calculate(3, 3, 3)
        self.assertEqual(t_type, "равносторонний")
        self.assertIsNone(err)

    def test_isosceles(self):
        t_type, _, err = TriangleCalculator.calculate(3, 3, 4)
        self.assertEqual(t_type, "равнобедренный")
        self.assertIsNone(err)

    def test_scalene(self):
        t_type, _, err = TriangleCalculator.calculate(3, 4, 5)
        self.assertEqual(t_type, "разносторонний")
        self.assertIsNone(err)

    def test_not_a_triangle(self):
        t_type, _, err = TriangleCalculator.calculate(1, 1, 10)
        self.assertEqual(t_type, "не треугольник")
        self.assertIsNotNone(err)

    def test_negative_sides(self):
        t_type, _, err = TriangleCalculator.calculate(-1, 2, 2)
        self.assertEqual(t_type, "не треугольник")
        self.assertIsNotNone(err)

    def test_non_numeric(self):
        t_type, _, err = TriangleCalculator.calculate("a", "b", "c")
        self.assertEqual(t_type, "")
        self.assertIsNotNone(err)

    def test_calculate_coords_returns_three_points(self):
        coords = calculate_coords(3, 4, 5)
        self.assertEqual(len(coords), 3)


# ---------- Юнит-тесты БД ----------

class TestTriangleDatabase(unittest.TestCase):

    def setUp(self):
        self.db = TriangleDatabase(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_and_get(self):
        self.db.add(3, 4, 5, "разносторонний", None)
        record = self.db.get(3, 4, 5)
        self.assertIsNotNone(record)
        self.assertEqual(record["triangle_type"], "разносторонний")
        self.assertIsNone(record["error_message"])

    def test_get_missing_returns_none(self):
        self.assertIsNone(self.db.get(9, 9, 9))

    def test_delete(self):
        self.db.add(3, 4, 5, "разносторонний", None)
        self.db.delete(3, 4, 5)
        self.assertIsNone(self.db.get(3, 4, 5))


# ---------- Юнит-тесты абстрактных интерфейсов ----------

class TestAbstractInterfaces(unittest.TestCase):

    def test_user_interface_is_abstract(self):
        with self.assertRaises(TypeError):
            UserInterface()

    def test_notifier_is_abstract(self):
        with self.assertRaises(TypeError):
            Notifier()

    def test_console_notifier_sends(self):
        n = ConsoleNotifier()
        self.assertTrue(n.send("hello"))

    @patch("builtins.input", side_effect=["3", "4", "5"])
    def test_console_ui_get_input(self, mock_input):
        ui = ConsoleUserInterface()
        self.assertEqual(ui.get_input(), ("3", "4", "5"))
        self.assertEqual(mock_input.call_count, 3)


# ---------- ИНТЕГРАЦИОННЫЕ тесты ----------

class TestControllerIntegration(unittest.TestCase):

    def setUp(self):
        self.db = TriangleDatabase(":memory:")
        self.ui = MagicMock()
        self.notifier = MagicMock()
        self.notifier.send.return_value = True
        self.controller = Controller(self.ui, self.db, self.notifier)

    def tearDown(self):
        self.db.close()

    def test_full_scenario_new_triangle(self):
        self.ui.get_input.return_value = ("3", "4", "5")
        result = self.controller.run()
        self.assertIn("разносторонний", result)
        self.assertIsNotNone(self.db.get(3.0, 4.0, 5.0))
        self.notifier.send.assert_called_once()

    def test_full_scenario_existing_in_db(self):
        self.db.add(3, 4, 5, "разносторонний", None)
        self.ui.get_input.return_value = ("3", "4", "5")
        result = self.controller.run()
        self.assertIn("разносторонний", result)
        self.notifier.send.assert_called_once()

    def test_full_scenario_non_numeric_input(self):
        self.ui.get_input.return_value = ("a", "b", "c")
        result = self.controller.run()
        self.assertIn("Ошибка", result)
        self.notifier.send.assert_called_once()

    def test_not_twice(self):
        self.ui.get_input.return_value = ("5", "5", "5")
        self.controller.run()
        self.controller.run()
        TriangleCalculator.calculate.assert_called_once()
