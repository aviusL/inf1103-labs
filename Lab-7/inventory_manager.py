import json
import os

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory

#inventory.json lives next to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(BASE_DIR, "inventory.json")

#weight given to older records that were saved before product types existed
DEFAULT_WEIGHT = 1.0


#file handling

def create_default_inventory():
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.0))
    inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, 0.1))
    inventory.add_product(PhysicalProduct("P003", "Keyboard", 45.00, 25, 0.8))
    inventory.add_product(DigitalProduct("P004", "Photo Editor", 89.90, 200, 1250.0))
    return inventory


def create_product_from_dict(item, price, stock):
    #uses the saved "type" to rebuild the right subclass, records without a type load as physical
    product_type = item.get("type", "physical")
    if product_type == "physical":
        return PhysicalProduct(item["id"], item["name"], price, stock, item.get("weight", DEFAULT_WEIGHT))
    if product_type == "digital":
        return DigitalProduct(item["id"], item["name"], price, stock, item["download_size"])
    raise ValueError(f"Unknown product type '{product_type}'.")


def load_inventory(filename=FILENAME):
    #builds an inventory of product objects from inventory.json, defaults if missing/corrupt
    if not os.path.exists(filename):
        print(f"{os.path.basename(filename)} not found.")
        print("Starting with default inventory.")
        return create_default_inventory()

    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except (json.JSONDecodeError, IOError):
        print("Error loading inventory file. Starting with default inventory.")
        return create_default_inventory()

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
            inventory.add_product(create_product_from_dict(item, price, stock))
        except (KeyError, TypeError, ValueError) as error:
            print(f"Skipping invalid record {item}: {error}")

    print(f"{os.path.basename(filename)} found.")
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory, filename=FILENAME):
    try:
        data = [product.to_dict() for product in inventory.get_products()]
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except IOError as error:
        print(f"Error saving inventory: {error}")
        return False


#menu actions (user input stays here, not in the classes)

def prompt_positive_float(prompt, label):
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


def add_product(inventory):
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
        elif inventory.search_product(product_id) is not None:
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

    #extra detail depends on the product type
    try:
        if product_type == "1":
            weight = prompt_positive_float("Weight (kg): ", "weight")
            product = PhysicalProduct(product_id, name, price, stock, weight)
        else:
            download_size = prompt_positive_float("Download Size (MB): ", "download size")
            product = DigitalProduct(product_id, name, price, stock, download_size)
        inventory.add_product(product)
        print("\nProduct added successfully!")
    except ValueError as error:
        print(f"\nError: {error}")


def update_stock(inventory):
    print("\nUpdate Stock")
    product = inventory.search_product(input("Enter Product ID: "))

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


def search_product(inventory):
    print("\nSearch Product")
    product = inventory.search_product(input("Enter Product ID: "))

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


def print_menu():
    print("\n---------- MENU ----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("--------------------------")


def main():
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")
    print()

    inventory = load_inventory()

    while True:
        print_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            if save_inventory(inventory):
                print(f"Inventory saved successfully to {os.path.basename(FILENAME)}.")
        elif choice == "6":
            print("\nSaving inventory before exit...")
            if save_inventory(inventory):
                print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option! Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
