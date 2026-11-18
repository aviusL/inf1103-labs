#lab 8 sections 6 and 7: Liskov Substitution and polymorphism through Product
#run with: python test_lsp_polymorphism.py

from supplier import Supplier
from product import Product
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


def heading(title: str) -> None:
    print(f"\n{title}")
    print("-" * 40)


def show_product_details(product: Product) -> None:
    #only uses what every Product promises, works the same for any subclass
    product.display_information()
    print(product.get_fulfilment_info())


def check_update_stock_contract(product: Product) -> None:
    #the expectation Product sets: any whole number >= 0 is accepted, anything else is ValueError
    for quantity in (0, 7, 120):
        product.update_stock(quantity)
        assert product.get_stock() == quantity
    for bad in (-1, 2.5, "10", True):
        try:
            product.update_stock(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{type(product).__name__} accepted {bad!r}")
    print(f"{type(product).__name__}: update_stock() keeps the Product contract")


def main() -> None:
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.0)
    editor = DigitalProduct("P300", "Photo Editor", 89.90, 200, supplier, 1250.0)

    heading("1. show_product_details(product: Product) with each subclass")
    for product in (laptop, editor):
        show_product_details(product)
        print()

    heading("2. Predict first: both types in one Inventory, one loop, no isinstance")
    inventory = Inventory()
    inventory.add_product(laptop)
    inventory.add_product(editor)
    for product in inventory.get_products():
        product.display_information()
        print(product.get_fulfilment_info())
        print()
    assert laptop.get_fulfilment_info().startswith("Physical")
    assert editor.get_fulfilment_info().startswith("Digital")

    heading("3. Inventory's own methods treat both as Product")
    inventory.display_all()
    print(f"find_product('P300') -> {type(inventory.find_product('P300')).__name__}")
    assert inventory.find_product("P001") is laptop
    assert inventory.find_product("P300") is editor

    heading("4. LSP: update_stock() means the same thing for both subclasses")
    for product in inventory.get_products():
        check_update_stock_contract(product)

    heading("5. LSP: return types match what Product promises")
    for product in inventory.get_products():
        info = product.get_fulfilment_info()
        data = product.to_dict()
        assert isinstance(info, str) and info
        assert isinstance(data, dict) and data["id"] == product.get_product_id()
        assert isinstance(product.get_price(), float) and isinstance(product.get_stock(), int)
        print(f"{type(product).__name__}: get_fulfilment_info() -> str, to_dict() -> dict")

    heading("6. An Order works with any Product as well")
    order = Order("ORD001")
    for product in inventory.get_products():
        product.update_stock(10)
        order.add_order_line(product, 2)
    order.display_order()
    assert abs(order.calculate_total() - (1200.00 * 2 + 89.90 * 2)) < 1e-9

    print("\nAll LSP and polymorphism checks passed.")


if __name__ == "__main__":
    main()
