import json
import os

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order import Order
from product import Product
from supplier import Supplier

#inventory.json and suppliers.json live next to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(BASE_DIR, "inventory.json")
SUPPLIERS_FILENAME = os.path.join(BASE_DIR, "suppliers.json")

#weight given to older records that were saved before product types existed
DEFAULT_WEIGHT = 1.0

#supplier given to older records that were saved before suppliers existed
UNASSIGNED_SUPPLIER_ID = "S000"


#suppliers (created and kept here, products only hold a reference to one)

def register_supplier(suppliers: dict[str, Supplier], supplier: Supplier) -> None:
    #keyed by lower-case ID so lookups are case-insensitive, same as product search
    suppliers[supplier.get_supplier_id().lower()] = supplier


def find_supplier(suppliers: dict[str, Supplier], supplier_id: str) -> Supplier | None:
    #returns the matching Supplier, or None if not found
    return suppliers.get(str(supplier_id).strip().lower())


def resolve_supplier(suppliers: dict[str, Supplier], supplier_id: str | None) -> Supplier:
    #every Product needs a Supplier, so a missing/unknown ID falls back to a placeholder
    supplier = find_supplier(suppliers, supplier_id) if supplier_id else None
    if supplier is None:
        supplier = find_supplier(suppliers, UNASSIGNED_SUPPLIER_ID)
    if supplier is None:
        supplier = Supplier(UNASSIGNED_SUPPLIER_ID, "Unassigned Supplier", "unassigned@example.com")
        register_supplier(suppliers, supplier)
    return supplier


def create_default_suppliers() -> dict[str, Supplier]:
    suppliers: dict[str, Supplier] = {}
    register_supplier(suppliers, Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example"))
    register_supplier(suppliers, Supplier("S002", "SoftWorks", "licensing@softworks.example"))
    return suppliers


def load_suppliers(filename: str = SUPPLIERS_FILENAME) -> dict[str, Supplier]:
    #builds the Supplier objects from suppliers.json, defaults if missing/corrupt
    if not os.path.exists(filename):
        print(f"{os.path.basename(filename)} not found.")
        print("Starting with default suppliers.")
        return create_default_suppliers()

    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except (json.JSONDecodeError, IOError):
        print("Error loading suppliers file. Starting with default suppliers.")
        return create_default_suppliers()

    suppliers: dict[str, Supplier] = {}
    for item in data:
        try:
            register_supplier(suppliers, Supplier(item["id"], item["name"], item["contact_email"]))
        except (KeyError, TypeError, ValueError) as error:
            print(f"Skipping invalid supplier record {item}: {error}")

    print(f"{os.path.basename(filename)} found.")
    print("Suppliers loaded successfully.")
    return suppliers


def save_suppliers(suppliers: dict[str, Supplier], filename: str = SUPPLIERS_FILENAME) -> bool:
    try:
        data = [supplier.to_dict() for supplier in suppliers.values()]
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except IOError as error:
        print(f"Error saving suppliers: {error}")
        return False


#file handling

def create_default_inventory(suppliers: dict[str, Supplier]) -> Inventory:
    hardware = resolve_supplier(suppliers, "S001")
    software = resolve_supplier(suppliers, "S002")

    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, hardware, 2.0))
    inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, hardware, 0.1))
    inventory.add_product(PhysicalProduct("P003", "Keyboard", 45.00, 25, hardware, 0.8))
    inventory.add_product(DigitalProduct("P004", "Photo Editor", 89.90, 200, software, 1250.0))
    return inventory


def create_product_from_dict(item: dict, price: float, stock: int,
                             suppliers: dict[str, Supplier]) -> Product:
    #uses the saved "type" to rebuild the right subclass, records without a type load as physical
    #the saved "supplier_id" is turned back into a reference to the existing Supplier object
    product_type = item.get("type", "physical")
    supplier = resolve_supplier(suppliers, item.get("supplier_id"))
    if product_type == "physical":
        return PhysicalProduct(item["id"], item["name"], price, stock, supplier,
                               item.get("weight", DEFAULT_WEIGHT))
    if product_type == "digital":
        return DigitalProduct(item["id"], item["name"], price, stock, supplier,
                              item["download_size"])
    raise ValueError(f"Unknown product type '{product_type}'.")


def load_inventory(suppliers: dict[str, Supplier], filename: str = FILENAME) -> Inventory:
    #builds an inventory of product objects from inventory.json, defaults if missing/corrupt
    if not os.path.exists(filename):
        print(f"{os.path.basename(filename)} not found.")
        print("Starting with default inventory.")
        return create_default_inventory(suppliers)

    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except (json.JSONDecodeError, IOError):
        print("Error loading inventory file. Starting with default inventory.")
        return create_default_inventory(suppliers)

    inventory = Inventory()
    for item in data:
        try:
            #sanitize bad values carried over from older files
            stock = item.get("stock", 0)
            price = item.get("price", 0)
            if isinstance(stock, int) and stock < 0:
                stock = 0
            if isinstance(price, (int, float)) and price <= 0:
                price = 1.00
            inventory.add_product(create_product_from_dict(item, price, stock, suppliers))
        except (KeyError, TypeError, ValueError) as error:
            print(f"Skipping invalid record {item}: {error}")

    print(f"{os.path.basename(filename)} found.")
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory: Inventory, filename: str = FILENAME) -> bool:
    try:
        data = [product.to_dict() for product in inventory.get_products()]
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except IOError as error:
        print(f"Error saving inventory: {error}")
        return False


#menu actions (user input stays here, not in the classes)

def prompt_positive_float(prompt: str, label: str) -> float:
    #keeps asking until a number greater than zero is entered
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print(f"Error: Invalid {label}. Please enter a valid decimal number.")
            continue
        if value <= 0:
            print(f"Error: {label.capitalize()} must be a positive number greater than zero!")
            continue
        return value


def add_supplier(suppliers: dict[str, Supplier]) -> Supplier:
    #creates a new Supplier on its own, before any Product refers to it
    print("\nAdd New Supplier")

    while True:
        supplier_id = input("Supplier ID: ").strip()
        if not supplier_id:
            print("Error: Supplier ID cannot be empty! Please try again.")
        elif find_supplier(suppliers, supplier_id) is not None:
            print("Error: Supplier ID already exists! Please enter a unique ID.")
        else:
            break

    while True:
        name = input("Supplier Name: ").strip()
        if name:
            break
        print("Error: Supplier Name cannot be empty! Please try again.")

    while True:
        try:
            #supplier validates its own email
            supplier = Supplier(supplier_id, name, input("Contact Email: "))
        except ValueError as error:
            print(f"Error: {error} Please try again.")
            continue
        register_supplier(suppliers, supplier)
        print("Supplier added successfully!")
        return supplier


def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier:
    #returns an existing Supplier object picked by ID, or a newly added one
    print("\nAvailable Suppliers")
    print("----------------------------------------")
    if not suppliers:
        print("No suppliers available.")
    for supplier in suppliers.values():
        print(supplier)
    print("----------------------------------------")

    while True:
        supplier_id = input("Supplier ID (or N to add a new supplier): ").strip()
        if supplier_id.lower() == "n":
            return add_supplier(suppliers)
        supplier = find_supplier(suppliers, supplier_id)
        if supplier is not None:
            return supplier
        print("Error: Supplier not found! Enter an ID from the list, or N.")


def add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nAdd New Product")

    while True:
        product_type = input("Product Type (1 = Physical, 2 = Digital): ").strip()
        if product_type in ("1", "2"):
            break
        print("Error: Please enter 1 for Physical or 2 for Digital.")

    while True:
        product_id = input("Product ID: ").strip()
        if not product_id:
            print("Error: Product ID cannot be empty! Please try again.")
        elif inventory.find_product(product_id) is not None:
            print("Error: Product ID already exists! Please enter a unique ID.")
        else:
            break

    while True:
        name = input("Product Name: ").strip()
        if name:
            break
        print("Error: Product Name cannot be empty! Please try again.")

    while True:
        try:
            price = float(input("Price: "))
        except ValueError:
            print("Error: Invalid price. Please enter a valid decimal number.")
            continue
        if price <= 0:
            print("Error: Price must be a positive number greater than zero!")
            continue
        break

    while True:
        try:
            stock = int(input("Stock Quantity: "))
        except ValueError:
            print("Error: Invalid stock. Please enter a whole non-negative integer.")
            continue
        if stock < 0:
            print("Error: Stock quantity cannot be negative!")
            continue
        break

    #the Supplier already exists, the new Product is only given a reference to it
    supplier = choose_supplier(suppliers)

    #extra detail depends on the product type
    try:
        if product_type == "1":
            weight = prompt_positive_float("Weight (kg): ", "weight")
            product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
        else:
            download_size = prompt_positive_float("Download Size (MB): ", "download size")
            product = DigitalProduct(product_id, name, price, stock, supplier, download_size)
        inventory.add_product(product)
        print("\nProduct added successfully!")
    except ValueError as error:
        print(f"\nError: {error}")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product = inventory.find_product(input("Enter Product ID: "))

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    while True:
        try:
            new_stock = int(input("\nNew Stock Quantity: "))
        except ValueError:
            print("Error: Stock quantity must be a valid whole non-negative integer!")
            continue
        try:
            #product validates and changes its own stock
            product.update_stock(new_stock)
        except ValueError as error:
            print(f"Error: {error} Please try again.")
            continue
        print("\nStock updated successfully!")
        return


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product = inventory.find_product(input("Enter Product ID: "))

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("----------------------------------------")
    product.display_information()
    print(product.get_fulfilment_info())
    #only products that sign the CanBeShipped contract have a shipping cost
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("----------------------------------------")
    print("Supplied By")
    product.display_supplier_information()
    print("----------------------------------------")


def remove_product(inventory: Inventory) -> None:
    print("\nRemove Product")
    product = inventory.find_product(input("Enter Product ID: "))

    if product is None:
        print("\nProduct not found.")
        return

    print(f"\n{product}")
    if input("Remove this product from the inventory? (y/n): ").strip().lower() != "y":
        print("Remove cancelled.")
        return

    #the inventory only lets go of its reference, the Product object is not destroyed
    inventory.remove_product(product.get_product_id())
    print("\nProduct removed from the inventory.")


def prompt_order_quantity(product: Product) -> int:
    #keeps asking until a whole number from 1 up to the available stock is entered
    while True:
        try:
            quantity = int(input(f"Quantity (1-{product.get_stock()}): "))
        except ValueError:
            print("Error: Quantity must be a whole number.")
            continue
        if quantity <= 0:
            print("Error: Quantity must be greater than zero!")
        elif quantity > product.get_stock():
            print(f"Error: Only {product.get_stock()} in stock.")
        else:
            return quantity


def create_order(inventory: Inventory, order_number: int) -> None:
    order = Order(f"ORD{order_number:03d}")
    print(f"\nCreate Order {order.get_order_id()}")
    print("Enter a Product ID to add it, or press Enter when done.")

    while True:
        product_id = input("\nProduct ID: ").strip()
        if not product_id:
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Error: Product not found!")
            continue
        if order.has_product(product_id):
            print("Error: Product is already in this order!")
            continue
        if product.get_stock() == 0:
            print("Error: Product is out of stock!")
            continue
        print(f"{product.get_name()} - ${product.get_price():.2f}")
        #the Order creates the OrderLine itself, only the Product and quantity are passed in
        order.add_order_line(product, prompt_order_quantity(product))

    if not order.get_order_lines():
        print("\nNo products added. Order discarded.")
        return

    order.display_order()
    if input("\nPlace this order? (y/n): ").strip().lower() != "y":
        #cancelling the order discards its lines with it
        order.cancel()
        print("Order cancelled.")
        return

    #same update_stock() call for every kind of Product (LSP)
    for order_line in order.get_order_lines():
        product = order_line.get_product()
        product.update_stock(product.get_stock() - order_line.get_quantity())
    print(f"\nOrder {order.get_order_id()} placed. Stock updated.")


def print_menu() -> None:
    print("\n---------- MENU ----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Create Order")
    print("7. Save Inventory")
    print("8. Exit")
    print("--------------------------")


def main() -> None:
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")
    print()

    #suppliers are loaded first so each product can be linked to its Supplier
    suppliers = load_suppliers()
    inventory = load_inventory(suppliers)
    #orders are not saved, numbering restarts each run
    order_number = 1

    while True:
        print_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory, suppliers)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            remove_product(inventory)
        elif choice == "6":
            create_order(inventory, order_number)
            order_number += 1
        elif choice == "7":
            print("\nSaving inventory...")
            if save_suppliers(suppliers) and save_inventory(inventory):
                print(f"Inventory saved successfully to {os.path.basename(FILENAME)}.")
        elif choice == "8":
            print("\nSaving inventory before exit...")
            if save_suppliers(suppliers) and save_inventory(inventory):
                print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option! Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
