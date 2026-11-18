#lab 8 section 4: composition between Order and OrderLine
#run with: python test_composition.py

from supplier import Supplier
from order import Order
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


def heading(title: str) -> None:
    print(f"\n{title}")
    print("-" * 40)


def main() -> None:
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.0)
    mouse = PhysicalProduct("P002", "Mouse", 25.50, 40, supplier, 0.1)
    editor = DigitalProduct("P300", "Photo Editor", 89.90, 200, supplier, 1250.0)

    heading("1. Order creates its own OrderLines from a Product and quantity")
    order_1 = Order("ORD001")
    order_1.add_order_line(laptop, 1)
    order_1.add_order_line(mouse, 2)
    order_1.add_order_line(editor, 3)
    order_1.display_order()
    expected_total = 1200.00 * 1 + 25.50 * 2 + 89.90 * 3
    assert abs(order_1.calculate_total() - expected_total) < 1e-9

    heading("2. Each subtotal is worked out by its OrderLine")
    for line in order_1.get_order_lines():
        print(f"{line.get_product().get_name()}: ${line.calculate_subtotal():.2f}")

    heading("3. Predict first: same Product in two Orders")
    order_2 = Order("ORD002")
    order_2.add_order_line(laptop, 2)
    line_in_1 = order_1.get_order_lines()[0]
    line_in_2 = order_2.get_order_lines()[0]
    print(f"OrderLine objects are the same: {line_in_1 is line_in_2}  "
          f"id={id(line_in_1)} / {id(line_in_2)}")
    print(f"Product objects are the same:   {line_in_1.get_product() is line_in_2.get_product()}  "
          f"id={id(line_in_1.get_product())} / {id(line_in_2.get_product())}")
    assert line_in_1 is not line_in_2
    assert line_in_1.get_product() is line_in_2.get_product() is laptop

    heading("4. Lines cannot be added or moved from outside the Order")
    lines = order_1.get_order_lines()
    print(f"get_order_lines() returns a {type(lines).__name__}")
    try:
        lines.append(line_in_2)
    except AttributeError as error:
        print(f"Rejected appending a line from ORD002: {error}")
    assert len(order_1.get_order_lines()) == 3

    heading("5. Remove a line through the Order: the Product is untouched")
    removed = order_1.remove_order_line("P002")
    print(f"remove_order_line('P002'): {removed}")
    order_1.display_order()
    print(f"Mouse still exists: {mouse}")
    assert removed and not order_1.has_product("P002")
    assert mouse.get_stock() == 40

    heading("6. Cancel an order: its lines go with it, Products remain")
    order_1.cancel()
    order_1.display_order()
    print(laptop)
    print(editor)
    assert order_1.get_order_lines() == () and order_1.calculate_total() == 0
    assert len(order_2.get_order_lines()) == 1

    heading("7. Invalid order lines are rejected")
    for bad_quantity in (0, -1, 1.5):
        try:
            order_2.add_order_line(mouse, bad_quantity)
        except ValueError as error:
            print(f"Rejected quantity {bad_quantity}: {error}")
        else:
            raise AssertionError("bad quantity accepted")
    try:
        order_2.add_order_line("P002", 1)
    except TypeError as error:
        print(f"Rejected product given as text: {error}")

    print("\nAll composition checks passed.")


if __name__ == "__main__":
    main()
