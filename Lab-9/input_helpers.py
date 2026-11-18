#lab 9 section 5.1: asking the user for input without crashing on bad entries

import math


def get_positive_float(prompt: str) -> float:
    #keeps asking until the user enters a number greater than zero.
    #float() raises ValueError for text like "abc" (exception handling);
    #the number itself is then checked with if statements (validation)
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")
            continue
        #"nan" and "inf" convert without an error but are not usable amounts
        if not math.isfinite(value):
            print("Please enter a valid number, e.g. 12.50")
            continue
        if value <= 0:
            print("Please enter a number greater than zero.")
            continue
        return value
