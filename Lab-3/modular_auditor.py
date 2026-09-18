

def get_valid_input():
    """Handles prompt and input validation.
    Returns:
        int: a valid input quantity, or
        str: 'quit' to end input, or
        None: if input is invalid.
    """
    user_input = input("Enter a stock quantity, or quit: ")

    if user_input.lower() == "quit":
        return "quit"

    try:
        cleaned = int(user_input)
        if cleaned <= 0:
            print("Inventory cannot be zero or a negative number.")
            return None
        return cleaned
    except ValueError:
        print("Invalid Input!")
        return None


def calculate_tax(amount):
    """Calculates 10% tax for a single delivery."""
    return amount * 0.10


def process_delivery(current_total, new_value):
    """Updates and returns the total inventory count after adding the delivery."""
    new_total = current_total + new_value
    tax = calculate_tax(new_value)
    
    print(f"Valid Input! Tax for this delivery (10%): {tax}")
    print(f"Inventory is now {new_total}")
    return new_total


def generate_report(total_units, failed_attempts):
    """Prints the final summary report."""
    print("\n--- Summary Report ---")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    inventory = 0
    failed_count = 0

    while True:
        user_choice = get_valid_input()

        if user_choice == "quit":
            generate_report(inventory, failed_count)
            break
        elif user_choice is None:
            failed_count += 1
        else:
            if (inventory + user_choice) >= 500:
                print("ALERT! Maximum capacity reached or exceeded.")
                failed_count += 1
                generate_report(inventory, failed_count)
                break
            else:
                inventory = process_delivery(inventory, user_choice)


if __name__ == "__main__":
    main()



    


