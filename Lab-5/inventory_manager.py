
import json
import os

FILENAME = "inventory.json"

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


def print_menu():
    """Display the system menu options."""
    print("\n---------- MENU ----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("--------------------------")


def display_all(inventory):
    """Placeholder for displaying products."""
    print("\n[Feature pending] Displaying products...")


def add_product(inventory):
    """Placeholder for adding a product."""
    print("\n[Feature pending] Add product functionality...")


def update_stock(inventory):
    """Placeholder for updating stock."""
    print("\n[Feature pending] Update stock functionality...")


def search_product(inventory):
    """Placeholder for searching products."""
    print("\n[Feature pending] Search product functionality...")


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