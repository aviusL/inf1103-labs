#lab 9 section 4: validation, each rule checked in the class that owns it

import unittest

from order import Order
from order_line import OrderLine
from product_factory import ProductFactory
from supplier import Supplier


class ValidationTests(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")

    def make(self, product_type: str, price: float = 10.00, stock: int = 5):
        return ProductFactory.create(product_type, "P001", "Test Item", price, stock, self.supplier)

    def test_price_must_be_greater_than_zero(self) -> None:
        for product_type in ("physical", "digital"):
            for bad_price in (0, -0.01, -25):
                with self.assertRaises(ValueError, msg=f"{product_type} price {bad_price}"):
                    self.make(product_type, price=bad_price)
            self.assertEqual(self.make(product_type, price=0.01).get_price(), 0.01)

    def test_price_must_be_a_real_number(self) -> None:
        for bad_price in ("abc", None, True, float("nan"), float("inf")):
            with self.assertRaises(ValueError, msg=f"price {bad_price!r}"):
                self.make("physical", price=bad_price)

    def test_stock_cannot_be_negative(self) -> None:
        for product_type in ("physical", "digital"):
            with self.assertRaises(ValueError):
                self.make(product_type, stock=-1)
            self.assertEqual(self.make(product_type, stock=0).get_stock(), 0)

    def test_stock_rule_also_applies_to_update_stock(self) -> None:
        #lab 9 section 4 predict-first: DigitalProduct keeps Product's rule (LSP)
        for product_type in ("physical", "digital"):
            product = self.make(product_type, stock=5)
            with self.assertRaises(ValueError):
                product.update_stock(-3)
            self.assertEqual(product.get_stock(), 5)

    def test_order_line_quantity_must_be_greater_than_zero(self) -> None:
        product = self.make("physical")
        for bad_quantity in (0, -1, 1.5, "2"):
            with self.assertRaises(ValueError, msg=f"quantity {bad_quantity!r}"):
                OrderLine(product, bad_quantity)
        self.assertEqual(OrderLine(product, 1).get_quantity(), 1)

    def test_order_rejects_bad_quantity_and_keeps_no_line(self) -> None:
        order = Order("ORD001")
        with self.assertRaises(ValueError):
            order.add_order_line(self.make("digital"), 0)
        self.assertEqual(order.get_order_lines(), ())


if __name__ == "__main__":
    unittest.main()
