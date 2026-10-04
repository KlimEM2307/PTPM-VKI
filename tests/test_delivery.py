import unittest
from src.Delivery import calculate_delivery_cost


class TestDelivery(unittest.TestCase):

    def test_weight_below_min(self):
        self.assertEqual(calculate_delivery_cost(0.05, 100, "обычный"), (-1, "0000-00-00"))

    def test_weight_above_max(self):
        self.assertEqual(calculate_delivery_cost(51, 100, "обычный"), (-1, "0000-00-00"))

    def test_distance_out_of_range(self):
        self.assertEqual(calculate_delivery_cost(5, 5001, "обычный"), (-1, "0000-00-00"))

    def test_invalid_package_type(self):
        self.assertEqual(calculate_delivery_cost(5, 100, "стеклянный"), (-1, "0000-00-00"))

    def test_base_cost_simple(self):
        cost, _ = calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_weight_over_5_adds_20_percent(self):
        cost, _ = calculate_delivery_cost(10, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_over_20_adds_50_percent(self):
        cost, _ = calculate_delivery_cost(25, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_fragile_adds_300(self):
        cost, _ = calculate_delivery_cost(1, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_express_should_be_more_expensive(self):
        normal, _ = calculate_delivery_cost(1, 100, "обычный", is_express=False)
        express, _ = calculate_delivery_cost(1, 100, "обычный", is_express=True)
        self.assertGreater(express, normal)

    def test_short_distance_min_one_day(self):
        _, date = calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(date, "2026-09-04")


if __name__ == "__main__":
    unittest.main()