import os

def calculate_tax(amount):
    # Calculate 10% tax on the delivery amount
    return amount * 0.10


def process_delivery(current_total, new_value):
    # Update running total and calculate tax for the current item
    new_total = current_total + new_value
    tax = calculate_tax(new_value)

    print(f"Valid Input! Tax for this delivery (10%): {tax:.2f}")
    print(f"Inventory is now {new_total}")
    return new_total


def load_inventory(filename="inventory.txt"):
    # Load inventory count and past transaction history if the file exists
    if not os.path.exists(filename):
        print("No prior inventory record found. Starting fresh inventory.")
        return 0, []

    try:
        with open(filename, "r") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
            if not lines:
                return 0, []
            
            total_inventory = int(lines[0])
            history = []
            if len(lines) > 1 and lines[1]:
                history = [int(val) for val in lines[1].split(",") if val.strip()]
                
            print(f"Loaded existing inventory: {total_inventory} units across {len(history)} past transactions.")
            return total_inventory, history
    except (ValueError, IOError):
        print("Warning: Could not load inventory file properly. Starting fresh.")
        return 0, []


def save_inventory(total, history, filename="inventory.txt"):
    # Save the updated inventory total and history list back to file
    try:
        with open(filename, "w") as file:
            file.write(f"{total}\n")
            file.write(",".join(map(str, history)) + "\n")
        print(f"Successfully saved inventory data to {filename}")
    except IOError as e:
        print(f"Error saving inventory to file: {e}")


def get_valid_input():
    user_input = input("Enter a stock quantity, or quit  :")

    if user_input.strip().lower() == "quit":
        return "quit"

    try:
        cleaned_input = int(user_input)
        if cleaned_input == 0:
            print("Quantity must be greater than zero.")
            return None
        elif cleaned_input < 0:
            print("Inventory cannot be a negative number.")
            return None
        return cleaned_input
    except ValueError:
        print("Invalid Input!")
        return None


def generate_report(total_units, failed_attempts, history):
    # Print final audit summary
    print("\n--- FINAL AUDIT SUMMARY ---")
    print(f"Total Inventory Units            :{total_units}")
    print(f"Total Transactions Recorded      :{len(history)}")
    print(f"Transaction History Log         :{history}")
    print(f"Number of Failed/Rejected Entries:{failed_attempts}")


def main():
    inventory, history = load_inventory()
    failed_count = 0

    while True:
        choice = get_valid_input()

        if choice == "quit":
            save_inventory(inventory, history)
            generate_report(inventory, failed_count, history)
            break
        elif choice is None:
            failed_count += 1
        else:
            if (inventory + choice) >= 500:
                print("ALERT! Maximum inventory capacity threshold (500) reached.")
                failed_count += 1
                save_inventory(inventory, history)
                generate_report(inventory, failed_count, history)
                break
            else:
                inventory = process_delivery(inventory, choice)
                history.append(choice)


if __name__ == "__main__":
    main()