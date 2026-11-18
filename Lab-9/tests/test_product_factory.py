#lab 9 section 3: factory pattern for creating products

import json
import os
import tempfile
import unittest
from unittest import mock

import inventory_manager
from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProductFactoryTests(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")

    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, self.supplier, weight=1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)
        self.assertEqual((product.get_product_id(), product.get_name()), ("P001", "Desk Lamp"))
        self.assertEqual((product.get_price(), product.get_stock(), product.get_weight()), (25.00, 10, 1.5))
        self.assertIs(product.get_supplier(), self.supplier)

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100, self.supplier,
                                        download_size=850.0)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 850.0)

    def test_type_ignores_case_and_spaces(self) -> None:
        self.assertIsInstance(ProductFactory.create(" Digital ", "D002", "Font Pack", 9.90, 5, self.supplier),
                              DigitalProduct)
        self.assertIsInstance(ProductFactory.create("PHYSICAL", "P002", "Chair", 89.00, 3, self.supplier),
                              PhysicalProduct)

    def test_defaults_used_when_detail_not_given(self) -> None:
        lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, self.supplier)
        editor = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100, self.supplier)
        self.assertEqual(lamp.get_weight(), ProductFactory.DEFAULT_WEIGHT)
        self.assertEqual(editor.get_download_size(), ProductFactory.DEFAULT_DOWNLOAD_SIZE)

    def test_unknown_type_raises_clear_value_error(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.00, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_product_still_validates_values_from_factory(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P009", "Free Lamp", 0, 10, self.supplier)


class ProgramUsesFactoryTests(unittest.TestCase):

    def test_menu_program_never_builds_a_subclass_directly(self) -> None:
        with open(os.path.join(BASE_DIR, "inventory_manager.py")) as file:
            source = file.read()
        self.assertNotIn("PhysicalProduct(", source)
        self.assertNotIn("DigitalProduct(", source)

    def test_default_inventory_is_built_through_factory(self) -> None:
        suppliers = inventory_manager.create_default_suppliers()
        with mock.patch.object(ProductFactory, "create", wraps=ProductFactory.create) as create:
            inventory = inventory_manager.create_default_inventory(suppliers)
        self.assertEqual(create.call_count, 4)
        self.assertEqual(inventory.count(), 4)

    def test_saved_inventory_loads_through_factory(self) -> None:
        records = [
            {"id": "P001", "name": "Laptop", "price": 1200.0, "stock": 15, "supplier_id": "S001",
             "type": "physical", "weight": 2.0},
            {"id": "P004", "name": "Photo Editor", "price": 89.9, "stock": 200, "supplier_id": "S002",
             "type": "digital", "download_size": 1250.0},
            {"id": "X001", "name": "Gift Wrap", "price": 2.0, "stock": 9, "type": "service"},
        ]
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            with open(path, "w") as file:
                json.dump(records, file)
            suppliers = inventory_manager.create_default_suppliers()
            with mock.patch("builtins.print"), \
                 mock.patch.object(ProductFactory, "create", wraps=ProductFactory.create) as create:
                inventory = inventory_manager.load_inventory(suppliers, path)
        self.assertEqual(create.call_count, 3)
        self.assertIsInstance(inventory.find_product("P001"), PhysicalProduct)
        self.assertIsInstance(inventory.find_product("P004"), DigitalProduct)
        #the unknown type was reported and skipped, not loaded
        self.assertIsNone(inventory.find_product("X001"))


if __name__ == "__main__":
    unittest.main()
