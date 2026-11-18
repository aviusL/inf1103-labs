from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    #strategy pattern: each way of discounting an order total is its own class.
    #an Order only calls apply(), it never checks which strategy it was given,
    #so a new discount is a new class here, not a change to Order

    @abstractmethod
    def apply(self, total: float) -> float:
        #returns the total after this discount
        pass


class NoDiscount(DiscountStrategy):

    def apply(self, total: float) -> float:
        return total

    def __str__(self) -> str:
        return "No discount"


class PercentageDiscount(DiscountStrategy):
    #takes a percentage off any total, e.g. PercentageDiscount(10) is 10% off

    def __init__(self, percentage: float) -> None:
        """raises ValueError unless percentage is a number above 0 and up to 100"""
        if isinstance(percentage, bool) or not isinstance(percentage, (int, float)):
            raise ValueError("Discount percentage must be a number.")
        if not 0 < percentage <= 100:
            raise ValueError("Discount percentage must be above 0 and at most 100.")
        self.__percentage: float = float(percentage)

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        #rounded to cents so totals print and compare as money
        return round(total * (1 - self.__percentage / 100), 2)

    def __str__(self) -> str:
        return f"{self.__percentage:g}% off"


class BulkDiscount(DiscountStrategy):
    #takes a fixed amount off totals at or above a threshold,
    #e.g. BulkDiscount(200, 20) is $20 off any total of $200 or more

    def __init__(self, threshold: float, amount: float) -> None:
        """raises ValueError if threshold is negative or amount is not above zero"""
        for value, label in ((threshold, "threshold"), (amount, "amount")):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"Bulk discount {label} must be a number.")
        if threshold < 0:
            raise ValueError("Bulk discount threshold cannot be negative.")
        if amount <= 0:
            raise ValueError("Bulk discount amount must be greater than zero.")
        self.__threshold: float = float(threshold)
        self.__amount: float = float(amount)

    def get_threshold(self) -> float:
        return self.__threshold

    def get_amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            #a discount never makes the total negative
            return max(total - self.__amount, 0.0)
        return total

    def __str__(self) -> str:
        return f"${self.__amount:.2f} off orders of ${self.__threshold:.2f} or more"
