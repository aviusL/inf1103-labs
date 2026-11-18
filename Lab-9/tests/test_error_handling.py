#lab 9 section 5: exception handling, the program fails gracefully

import ast
import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

from input_helpers import get_positive_float
from inventory import Inventory
from product_factory import ProductFactory
from product_loader import load_products
from supplier import Supplier

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LAB_CSV = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


def run_quietly(function, *args):
    #calls function and returns (its result, everything it printed as a list of lines)
    output = io.StringIO()
    with redirect_stdout(output):
        result = function(*args)
    return result, output.getvalue().splitlines()


class UserInputTests(unittest.TestCase):

    def ask(self, *entries: str) -> tuple[float, list[str]]:
        with mock.patch("builtins.input", side_effect=list(entries)):
            return run_quietly(get_positive_float, "Price: ")

    def test_keeps_asking_until_valid_price(self) -> None:
        value, printed = self.ask("abc", "-5", "12.50")
        self.assertEqual(value, 12.50)
        self.assertEqual(printed, ["Please enter a valid number, e.g. 12.50",
                                   "Please enter a number greater than zero."])

    def test_zero_nan_and_inf_are_not_accepted(self) -> None:
        value, printed = self.ask("0", "nan", "inf", "", "3")
        self.assertEqual(value, 3.0)
        self.assertEqual(len(printed), 4)

    def test_valid_first_entry_prints_nothing(self) -> None:
        self.assertEqual(self.ask("49.90"), (49.90, []))


class LoadProductsTests(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
        self.inventory = Inventory()
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)

    def write_csv(self, text: str) -> str:
        path = os.path.join(self.folder.name, "products.csv")
        with open(path, "w", newline="") as file:
            file.write(text)
        return path

    def load(self, path: str) -> list[str]:
        return run_quietly(load_products, path, self.inventory, self.supplier)[1]

    def test_lab_file_loads_valid_rows_and_skips_bad_ones(self) -> None:
        printed = self.load(self.write_csv(LAB_CSV))
        self.assertEqual(printed, ["Skipping row 4: Unknown product type: service",
                                   "Skipping row 5: Price 'abc' is not a number.",
                                   "3 products loaded.",
                                   "Load attempt finished."])
        self.assertEqual([p.get_product_id() for p in self.inventory.get_products()],
                         ["P001", "D001", "P003"])

    def test_products_are_built_through_the_factory(self) -> None:
        path = self.write_csv(LAB_CSV)
        with mock.patch.object(ProductFactory, "create", wraps=ProductFactory.create) as create:
            self.load(path)
        #every row that got past the number checks went to the factory, the service row included
        self.assertEqual(create.call_count, 4)

    def test_project_products_csv_matches_the_lab_file(self) -> None:
        with open(os.path.join(BASE_DIR, "products.csv"), newline="") as file:
            self.assertEqual(file.read().replace("\r\n", "\n"), LAB_CSV)

    def test_missing_file_is_reported_not_raised(self) -> None:
        printed = self.load(os.path.join(self.folder.name, "renamed.csv"))
        self.assertEqual(printed[0], f"Products file not found: {os.path.join(self.folder.name, 'renamed.csv')}")
        self.assertEqual(printed[-1], "Load attempt finished.")
        self.assertEqual(len(printed), 2)
        self.assertEqual(self.inventory.count(), 0)

    def test_other_bad_rows_are_skipped(self) -> None:
        printed = self.load(self.write_csv(
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,25.00,10\n"
            "\n"
            "physical,P001,Duplicate Lamp,25.00,10\n"
            "digital,D001,Font Pack,9.90\n"
            "physical,P002,Chair,0,3\n"
            "physical,P003,Stand,39.50,2.5\n"
            "digital,D002,Plugin,19.90,-1\n"))
        self.assertEqual(self.inventory.count(), 1)
        self.assertEqual(printed[-2:], ["1 products loaded.", "Load attempt finished."])
        skipped = printed[:-2]
        self.assertEqual(len(skipped), 5)
        self.assertTrue(all(line.startswith("Skipping row") for line in skipped))
        self.assertIn("already exists", skipped[0])
        self.assertIn("expected 5 values, found 4", skipped[1])
        self.assertIn("'2.5' is not a whole number", skipped[3])

    def test_header_only_file_loads_nothing(self) -> None:
        printed = self.load(self.write_csv("product_type,product_id,name,price,stock_quantity\n"))
        self.assertEqual(printed, ["0 products loaded.", "Load attempt finished."])


class ProgramRobustnessTests(unittest.TestCase):

    def test_every_except_names_a_specific_exception(self) -> None:
        broad = []
        for folder in (BASE_DIR, os.path.join(BASE_DIR, "tests")):
            for name in sorted(os.listdir(folder)):
                if not name.endswith(".py"):
                    continue
                with open(os.path.join(folder, name)) as file:
                    tree = ast.parse(file.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.ExceptHandler):
                        caught = ast.unparse(node.type) if node.type else "<bare except>"
                        if caught in ("<bare except>", "Exception", "BaseException"):
                            broad.append(f"{name}:{node.lineno} {caught}")
        self.assertEqual(broad, [])

    def test_menu_program_stops_cleanly_when_input_ends(self) -> None:
        #e.g. docker run without -it: no traceback, nothing saved
        result = subprocess.run([sys.executable, os.path.join(BASE_DIR, "inventory_manager.py")],
                                stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("Program terminated without saving.", result.stdout)


if __name__ == "__main__":
    unittest.main()
