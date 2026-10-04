import unittest
from src.triangle import get_triangle_type_and_coords


class TestTriangle(unittest.TestCase):

    def test_equilateral_triangle(self):
        t, _ = get_triangle_type_and_coords("3", "3", "3")
        self.assertEqual(t, "равносторонний")

    def test_isosceles_ab(self):
        t, _ = get_triangle_type_and_coords("5", "5", "6")
        self.assertEqual(t, "равнобедренный")

    def test_isosceles_ac(self):
        t, _ = get_triangle_type_and_coords("5", "6", "5")
        self.assertEqual(t, "равнобедренный")

    def test_isosceles_bc(self):
        t, _ = get_triangle_type_and_coords("6", "5", "5")
        self.assertEqual(t, "равнобедренный")

    def test_scalene_triangle(self):
        t, _ = get_triangle_type_and_coords("3", "4", "5")
        self.assertEqual(t, "разносторонний")

    def test_not_triangle_sum_too_small(self):
        t, _ = get_triangle_type_and_coords("1", "2", "10")
        self.assertEqual(t, "не треугольник")

    def test_not_triangle_equal_sum(self):
        t, _ = get_triangle_type_and_coords("1", "2", "3")
        self.assertEqual(t, "не треугольник")

    def test_zero_side(self):
        t, _ = get_triangle_type_and_coords("0", "5", "5")
        self.assertEqual(t, "не треугольник")

    def test_negative_side(self):
        t, _ = get_triangle_type_and_coords("-3", "4", "5")
        self.assertEqual(t, "не треугольник")

    def test_non_numeric_returns_empty_type(self):
        t, _ = get_triangle_type_and_coords("a", "b", "c")
        self.assertEqual(t, "")

    def test_non_numeric_coords_minus_two(self):
        _, c = get_triangle_type_and_coords("a", "b", "c")
        self.assertEqual(c, [(-2, -2), (-2, -2), (-2, -2)])

    def test_invalid_number_coords_minus_one(self):
        _, c = get_triangle_type_and_coords("1", "2", "10")
        self.assertEqual(c, [(-1, -1), (-1, -1), (-1, -1)])

    def test_coords_count_is_three(self):
        _, c = get_triangle_type_and_coords("3", "4", "5")
        self.assertEqual(len(c), 3)

    def test_coords_are_ints(self):
        _, c = get_triangle_type_and_coords("3", "4", "5")
        for x, y in c:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)

    def test_first_vertex_at_origin(self):
        _, c = get_triangle_type_and_coords("3", "4", "5")
        self.assertEqual(c[0], (0, 0))

    def test_coords_fit_in_100px(self):
        _, c = get_triangle_type_and_coords("3", "4", "5")
        for x, y in c:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)

    def test_equilateral_second_vertex_x_is_100(self):
        _, c = get_triangle_type_and_coords("3", "3", "3")
        self.assertEqual(c[1][0], 100)

    def test_float_sides(self):
        t, c = get_triangle_type_and_coords("3.5", "4.5", "5.5")
        self.assertEqual(t, "разносторонний")
        self.assertEqual(len(c), 3)

    def test_large_triangle_fits_field(self):
        _, c = get_triangle_type_and_coords("50", "60", "70")
        for x, y in c:
            self.assertLessEqual(x, 100)
            self.assertLessEqual(y, 100)

    def test_empty_string_is_invalid(self):
        t, _ = get_triangle_type_and_coords("", "5", "5")
        self.assertEqual(t, "")


if __name__ == "__main__":
    unittest.main()