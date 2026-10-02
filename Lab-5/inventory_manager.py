
import json
import os

# Dynamically set FILENAME relative to this script's folder location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(BASE_DIR, "inventory.json")

DEFAULT_INVENTORY = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
]


def load_inventory(filename=FILENAME):
    """Load inventory from JSON file if available; otherwise return default inventory."""
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                print(f"{filename} found.")
                print("Inventory loaded successfully.")
                return data
        except (json.JSONDecodeError, IOError):
            print("Error loading inventory file. Starting with default products.")
            return DEFAULT_INVENTORY.copy()
    else:
        print(f"{filename} not found.")
        print("Starting with default inventory.")
        return DEFAULT_INVENTORY.copy()


def save_inventory(inventory, filename=FILENAME):
    """Save inventory list to inventory.json."""
    try:
        with open(filename, "w") as file:
            json.dump(inventory, file, indent=4)
        print(f"Inventory saved successfully to {filename}.")
    except IOError as e:
        print(f"Error saving inventory: {e}")


def display_all(inventory):
    """Display all products formatted as ID | Name | Price | Stock."""
    print("\nCurrent Inventory")
    print("----------------------------------------")
    if not inventory:
        print("No products available.")
    else:
        for item in inventory:
            print(f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print("----------------------------------------")


def add_product(inventory):
    """Prompt user to add a new product dictionary to inventory."""
    print("\nAdd New Product")
    prod_id = input("Product ID: ").strip()

    for item in inventory:
        if item["id"].lower() == prod_id.lower():
            print("Error: Product ID already exists!")
            return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid numerical input for price or stock quantity.")
        return

    new_item = {
        "id": prod_id,
        "name": name,
        "price": price,
        "stock": stock
    }
    inventory.append(new_item)
    print("\nProduct added successfully!")


def update_stock(inventory):
    """Search by ID and update stock quantity for an existing product."""
    print("\nUpdate Stock")
    prod_id = input("Enter Product ID: ").strip()

    for item in inventory:
        if item["id"].lower() == prod_id.lower():
            print("\nProduct Found:")
            print(f"Name: {item['name']}")
            print(f"Current Stock: {item['stock']}")
            try:
                new_stock = int(input("\nNew Stock Quantity: "))
                item["stock"] = new_stock
                print("\nStock updated successfully!")
            except ValueError:
                print("Invalid quantity entered.")
            return

    print("Product not found.")


def search_product(inventory):
    """Search for a product by its ID and display its full details."""
    print("\nSearch Product")
    prod_id = input("Enter Product ID: ").strip()

    for item in inventory:
        if item["id"].lower() == prod_id.lower():
            print("\nProduct Found")
            print("----------------------------------------")
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock: {item['stock']}")
            print("----------------------------------------")
            return

    print("\nProduct not found.")


def print_menu():
    """Display the main system menu."""
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

    inventory = load_inventory()

    while True:
        print_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option! Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()