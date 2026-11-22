import unittest
from converter import Converter

class TestConverter(unittest.TestCase):

    # 1. Проверка верхней границы (x >= 100.7 -> 1000)
    def test_upper_boundary_exact(self):
        self.assertEqual(Converter.do(100.7), 1000)

    def test_upper_boundary_above(self):
        self.assertEqual(Converter.do(150.5), 1000)

    # 2. Проверка положительного диапазона (0 < x < 100.7 -> int(x))
    def test_positive_just_below_boundary(self):
        self.assertEqual(Converter.do(100.6), 100)

    def test_positive_middle(self):
        self.assertEqual(Converter.do(50.9), 50)

    def test_positive_small(self):
        self.assertEqual(Converter.do(0.1), 0)

    # 3. Проверка исключения при x == 0.0
    def test_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            Converter.do(0.0)

    # 4. Проверка отрицательного диапазона (-30.4 <= x < 0 -> int(x) - 5)
    def test_negative_boundary_exact(self):
        # int(-30.4) = -30; -30 - 5 = -35
        self.assertEqual(Converter.do(-30.4), -35)

    def test_negative_close_to_zero(self):
        # int(-0.1) = 0; 0 - 5 = -5
        self.assertEqual(Converter.do(-0.1), -5)

    def test_negative_middle(self):
        # int(-15.5) = -15; -15 - 5 = -20
        self.assertEqual(Converter.do(-15.5), -20)

    # 5. Проверка нижней границы (x <= -30.5 -> -2000)
    def test_lower_boundary_exact(self):
        self.assertEqual(Converter.do(-30.5), -2000)

    def test_lower_boundary_below(self):
        self.assertEqual(Converter.do(-100.9), -2000)

if __name__ == '__main__':
    unittest.main()


#python -m unittest -v test_converter.py
#pip install coverage
#coverage run -m unittest test_converter.py
#coverage report -m