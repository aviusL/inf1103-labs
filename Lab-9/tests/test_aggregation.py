#lab 8 section 3: aggregation between Inventory and Product
#run on its own from the Lab-9 folder with: python -m tests.test_aggregation

from supplier import Supplier
from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


def heading(title: str) -> None:
    print(f"\n{title}")
    print("-" * 40)


def main() -> None:
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")

    heading("1. Product is created before any Inventory exists")
    keyboard = PhysicalProduct("P003", "Keyboard", 45.00, 25, supplier, 0.8)
    print(keyboard)

    heading("2. Add the Product to Inventory A")
    inventory_a = Inventory()
    inventory_b = Inventory()
    inventory_a.add_product(keyboard)
    print(f"A contains keyboard: {inventory_a.contains(keyboard)}  (A has {inventory_a.count()})")
    assert inventory_a.contains(keyboard)

    heading("3. Predict first: remove it from Inventory A, is it still usable?")
    removed = inventory_a.remove_product("P003")
    print(f"A contains keyboard: {inventory_a.contains(keyboard)}  (A has {inventory_a.count()})")
    print(f"remove_product returned the same object: {removed is keyboard}")
    keyboard.update_stock(30)
    keyboard.display_information()
    assert removed is keyboard
    assert not inventory_a.contains(keyboard)
    assert keyboard.get_stock() == 30

    heading("4. Add the same Product object to Inventory B")
    inventory_b.add_product(keyboard)
    found = inventory_b.find_product("p003")
    print(f"B contains keyboard: {inventory_b.contains(keyboard)}")
    print(f"found in B is the same object: {found is keyboard}  id={id(found)} / {id(keyboard)}")
    assert found is keyboard

    heading("5. Transfer between inventories moves the object, nothing is copied")
    editor = DigitalProduct("P300", "Photo Editor", 89.90, 200, supplier, 1250.0)
    inventory_b.add_product(editor)
    moved = inventory_b.transfer_product("P300", inventory_a)
    print(f"transfer_product returned: {moved}")
    print(f"A contains editor: {inventory_a.contains(editor)}  B contains editor: {inventory_b.contains(editor)}")
    assert moved and inventory_a.contains(editor) and not inventory_b.contains(editor)
    assert inventory_a.find_product("P300") is editor

    heading("6. Empty an inventory: the products still exist")
    for product in inventory_a.get_products() + inventory_b.get_products():
        removed = (inventory_a.remove_product(product.get_product_id())
                   or inventory_b.remove_product(product.get_product_id()))
        assert removed is product
    print(f"A has {inventory_a.count()}, B has {inventory_b.count()}")
    del inventory_a, inventory_b
    print(keyboard)
    print(editor)
    assert keyboard.get_name() == "Keyboard" and editor.get_name() == "Photo Editor"

    heading("7. Lookups that find nothing return None")
    empty = Inventory()
    print(f"find_product('P999'): {empty.find_product('P999')}")
    print(f"remove_product('P999'): {empty.remove_product('P999')}")
    assert empty.find_product("P999") is None and empty.remove_product("P999") is None

    print("\nAll aggregation checks passed.")


if __name__ == "__main__":
    main()
