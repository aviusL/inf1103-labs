#lab 9 section 2: strategy pattern for order discounts

import inspect
import os
import unittest

from discount_strategy import BulkDiscount, DiscountStrategy, NoDiscount, PercentageDiscount
from student_discount import StudentDiscount
from order import Order
from physical_product import PhysicalProduct
from supplier import Supplier

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_order_totalling_250(order_id: str = "ORD001", discount: DiscountStrategy | None = None) -> Order:
    #2 x $100 + 1 x $50 = $250 before discount
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
    order = Order(order_id, discount)
    order.add_order_line(PhysicalProduct("P001", "Monitor", 100.00, 10, supplier, 4.0), 2)
    order.add_order_line(PhysicalProduct("P002", "Webcam", 50.00, 10, supplier, 0.3), 1)
    return order


class DiscountStrategyTests(unittest.TestCase):

    def test_no_discount_returns_total_unchanged(self) -> None:
        self.assertEqual(NoDiscount().apply(250.00), 250.00)

    def test_percentage_discount_takes_percentage_off(self) -> None:
        self.assertAlmostEqual(PercentageDiscount(10).apply(250.00), 225.00)
        self.assertAlmostEqual(PercentageDiscount(12.5).apply(80.00), 70.00)

    def test_bulk_discount_only_at_or_above_threshold(self) -> None:
        bulk = BulkDiscount(200, 20)
        self.assertAlmostEqual(bulk.apply(250.00), 230.00)
        self.assertAlmostEqual(bulk.apply(200.00), 180.00)
        self.assertAlmostEqual(bulk.apply(199.99), 199.99)

    def test_bulk_discount_never_goes_below_zero(self) -> None:
        self.assertEqual(BulkDiscount(0, 50).apply(30.00), 0.0)

    def test_invalid_strategy_settings_are_rejected(self) -> None:
        for bad in (0, -5, 101, "10", True):
            with self.assertRaises(ValueError, msg=f"PercentageDiscount({bad!r})"):
                PercentageDiscount(bad)
        for threshold, amount in ((-1, 20), (200, 0), (200, -5), ("200", 20)):
            with self.assertRaises(ValueError, msg=f"BulkDiscount({threshold!r}, {amount!r})"):
                BulkDiscount(threshold, amount)

    def test_discount_strategy_cannot_be_created_directly(self) -> None:
        with self.assertRaises(TypeError):
            DiscountStrategy()


class OrderUsesStrategyTests(unittest.TestCase):

    def test_order_defaults_to_no_discount(self) -> None:
        order = make_order_totalling_250()
        self.assertIsInstance(order.get_discount(), NoDiscount)
        self.assertAlmostEqual(order.calculate_total(), 250.00)

    def test_total_goes_through_the_given_strategy(self) -> None:
        order = make_order_totalling_250(discount=BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_subtotal(), 250.00)
        self.assertAlmostEqual(order.calculate_total(), 230.00)

    def test_set_discount_changes_strategy_on_existing_order(self) -> None:
        order = make_order_totalling_250(discount=BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.00)
        self.assertEqual(len(order.get_order_lines()), 2)

    def test_order_only_accepts_a_discount_strategy(self) -> None:
        with self.assertRaises(TypeError):
            Order("ORD001", "bulk")
        order = make_order_totalling_250()
        with self.assertRaises(TypeError):
            order.set_discount(0.1)
        self.assertIsInstance(order.get_discount(), NoDiscount)

    def test_order_has_no_discount_if_elif_logic(self) -> None:
        total_source = inspect.getsource(Order.calculate_total)
        self.assertNotIn("if ", total_source)
        with open(os.path.join(BASE_DIR, "order.py")) as file:
            order_source = file.read()
        for concrete in ("PercentageDiscount", "BulkDiscount", "StudentDiscount", "discount_type"):
            self.assertNotIn(concrete, order_source)

    def test_two_orders_can_share_one_strategy_object(self) -> None:
        ten_percent = PercentageDiscount(10)
        first = make_order_totalling_250("ORD001", ten_percent)
        second = make_order_totalling_250("ORD002", ten_percent)
        second.add_order_line(PhysicalProduct("P003", "Cable", 10.00, 5,
                                              first.get_order_lines()[0].get_product().get_supplier(), 0.1), 5)
        self.assertIs(first.get_discount(), second.get_discount())
        self.assertAlmostEqual(first.calculate_total(), 225.00)
        self.assertAlmostEqual(second.calculate_total(), 270.00)


class ExtendWithoutModifyingTests(unittest.TestCase):

    def test_student_discount_works_with_unchanged_order(self) -> None:
        order = make_order_totalling_250(discount=StudentDiscount())
        self.assertAlmostEqual(order.calculate_total(), 237.50)

    def test_any_new_strategy_class_works_with_order(self) -> None:
        #a strategy written only inside this test, Order has never seen it
        class HalfPrice(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total / 2

        order = make_order_totalling_250(discount=HalfPrice())
        self.assertAlmostEqual(order.calculate_total(), 125.00)


if __name__ == "__main__":
    unittest.main()
