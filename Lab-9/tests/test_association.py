#lab 8 section 2: association between Supplier and Product
#run on its own from the Lab-9 folder with: python -m tests.test_association

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


def heading(title: str) -> None:
    print(f"\n{title}")
    print("-" * 40)


def main() -> None:
    heading("1. Supplier is created on its own, before any Product exists")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
    supplier.display_information()

    heading("2. Both products are given the same existing Supplier object")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.0)
    editor = DigitalProduct("P300", "Photo Editor", 89.90, 200, supplier, 1250.0)
    print(laptop)
    print(editor)

    heading("3. Supplier information displayed through each Product")
    products: list[Product] = [laptop, editor]
    for product in products:
        print(f"{product.get_name()} is supplied by:")
        product.display_supplier_information()
        print()

    heading("4. Supplier and Products are separate objects")
    print(f"laptop.get_supplier() is supplier: {laptop.get_supplier() is supplier}")
    print(f"editor.get_supplier() is supplier: {editor.get_supplier() is supplier}")
    print(f"laptop is supplier: {laptop is supplier}")
    print(f"id(supplier)={id(supplier)}  id(laptop)={id(laptop)}  id(editor)={id(editor)}")
    assert laptop.get_supplier() is supplier
    assert editor.get_supplier() is supplier
    assert laptop is not supplier and editor is not supplier
    assert not isinstance(supplier, Product)

    heading("5. Predict first: del supplier, then ask each Product for its supplier")
    del supplier
    for product in products:
        print(f"{product.get_name()} is supplied by:")
        product.display_supplier_information()
        print()
    assert laptop.get_supplier().get_name() == "TechSource Pte Ltd"
    assert laptop.get_supplier() is editor.get_supplier()

    heading("6. The Supplier does not depend on its Products either")
    same_supplier = laptop.get_supplier()
    del laptop, editor, product, products
    same_supplier.display_information()
    assert same_supplier.get_supplier_id() == "S001"

    heading("7. A Product needs a Supplier object, not just a name or ID")
    for not_a_supplier in ("TechSource Pte Ltd", "S001", None):
        try:
            PhysicalProduct("P002", "Mouse", 25.50, 40, not_a_supplier, 0.1)
        except TypeError as error:
            print(f"Rejected supplier={not_a_supplier!r}: {error}")
        else:
            raise AssertionError("a non-Supplier value was accepted")

    print("\nAll association checks passed.")


if __name__ == "__main__":
    main()
