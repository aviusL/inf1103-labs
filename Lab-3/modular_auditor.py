
def get_valid_input():
    """Handles user input and returns an integer or 'quit' signal."""
    user_input = input("Enter a stock quantity, or quit: ")
    
    if user_input.lower() == "quit":
        return "quit"
    
    try:
        return int(user_input)
    except ValueError:
        print("Invalid Input!")
        return None


def calculate_tax(amount):
    """Calculates 10% tax for a single delivery."""
    return amount * 0.10


def process_delivery(current_total, new_value):
    """Updates total stock and displays delivery tax details."""
    new_total = current_total + new_value
    tax = calculate_tax(new_value)
    
    print(f"Valid Input! Tax for this delivery (10%): {tax}")
    print(f"Inventory is now {new_total}")
    return new_total


def generate_report(total_units, failed_attempts):
    """Prints final summary (Stub)."""
    # TODO: Expand reporting formatting and validation rules in Commit 3
    print(f"Total: {total_units}, Failed: {failed_attempts}")


def main():
    inventory = 0
    failed_count = 0

    while True:
        choice = get_valid_input()

        if choice == "quit":
            generate_report(inventory, failed_count)
            break
        elif choice is None:
            failed_count += 1
        else:
            inventory = process_delivery(inventory, choice)


if __name__ == "__main__":
    main()