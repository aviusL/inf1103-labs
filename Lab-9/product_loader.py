#lab 9 section 5.2: loading products from a CSV file without crashing

import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier

#product_type,product_id,name,price,stock_quantity
EXPECTED_COLUMNS = 5


def to_number(text: str, label: str, convert: type) -> float | int:
    #turns the CSV text into a number, with a message a user can understand
    try:
        return convert(text)
    except ValueError:
        kind = "whole number" if convert is int else "number"
        raise ValueError(f"{label} '{text}' is not a {kind}.") from None


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """read products from a CSV file into inventory, building each one through ProductFactory.

    a missing file is reported instead of crashing the program.
    a bad row (wrong number of values, unknown type, value that is not a number,
    duplicate ID) is reported and skipped, and the remaining rows still load
    """
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  #skip the header row
            for row in reader:
                if not row:
                    continue  #blank line
                try:
                    if len(row) != EXPECTED_COLUMNS:
                        raise ValueError(f"expected {EXPECTED_COLUMNS} values, found {len(row)}.")
                    product_type, product_id, name, price, stock_quantity = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    to_number(price, "Price", float),
                                                    to_number(stock_quantity, "Stock quantity", int),
                                                    supplier)
                    inventory.add_product(product)
                except ValueError as error:
                    #report this row and carry on with the next one
                    print(f"Skipping row {reader.line_num}: {error}")
                else:
                    loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
