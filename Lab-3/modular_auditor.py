
def calculate_tax(amount):
    """Calculates 10% tax for a single delivery amount."""
    return amount * 0.10


def process_delivery(current_total, new_value):
    """Updates and returns total stock while computing and displaying tax details."""
    new_total = current_total + new_value
    tax = calculate_tax(new_value)
    
    print(f"Valid Input! Tax for this delivery (10%): {tax}")
    print(f"Inventory is now {new_total}")
    return new_total


def get_valid_input():
    """Handles prompt and input validation.
    
    Returns:
        int: A valid stock quantity (> 0), or
        str: 'quit' signal, or
        None: If input is invalid/negative.
    """
    user_input = input("Enter a stock quantity, or quit  :")
    
    if user_input.strip().lower() == "quit":
        return "quit"
    
    try:
        cleaned_input = int(user_input)
        if cleaned_input < 1:
            print("Inventory cannot be a negative number.")
            return None
        return cleaned_input
    except ValueError:
        print("Invalid Input!")
        return None


def generate_report(total_units, failed_attempts):
    """Prints the final audit summary report."""
    print(f"Total Deliveries Processed :{total_units}")
    print(f"Number of Failed/Rejected Entries :{failed_attempts}")


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
            if (inventory + choice) >= 500:
                print("ALERT!")
                failed_count += 1
                generate_report(inventory, failed_count)
                break
            else:
                inventory = process_delivery(inventory, choice)


if __name__ == "__main__":
    main()