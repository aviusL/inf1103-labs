from product import Product
from order_line import OrderLine
from discount_strategy import DiscountStrategy, NoDiscount


class Order:
    #composition: an Order creates and owns its OrderLine objects.
    #lines are made inside add_order_line(), never passed in from outside,
    #and they go away with the order when it is cancelled.
    #the discount is a DiscountStrategy the order is given and uses (strategy pattern);
    #Order has no if/elif about discount types

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        """raises ValueError if order_id is empty, TypeError if discount is not a DiscountStrategy.

        with no discount given, the order uses NoDiscount()
        """
        order_id = str(order_id).strip()
        if not order_id:
            raise ValueError("Order ID cannot be empty.")
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = self.__validate_discount(
            discount if discount is not None else NoDiscount())

    # private

    @staticmethod
    def __validate_discount(discount: DiscountStrategy) -> DiscountStrategy:
        if not isinstance(discount, DiscountStrategy):
            raise TypeError("Discount must be a DiscountStrategy object.")
        return discount

    # getters

    def get_order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        #read-only view: callers can look at the lines but cannot add, remove or move them
        return tuple(self.__order_lines)

    def get_discount(self) -> DiscountStrategy:
        return self.__discount

    # public

    def set_discount(self, discount: DiscountStrategy) -> None:
        #swaps the strategy on an existing order, the lines are not touched
        self.__discount = self.__validate_discount(discount)

    def add_order_line(self, product: Product, quantity: int) -> None:
        #the Order builds the line itself, so every line belongs to exactly one Order
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        #removes the first line for that product, the Product itself is untouched
        product_id = str(product_id).strip().lower()
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id().lower() == product_id:
                self.__order_lines.remove(order_line)
                return True
        return False

    def has_product(self, product_id: str) -> bool:
        product_id = str(product_id).strip().lower()
        return any(line.get_product().get_product_id().lower() == product_id
                   for line in self.__order_lines)

    def calculate_subtotal(self) -> float:
        #before any discount, each line works out its own subtotal
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def calculate_total(self) -> float:
        #the strategy decides the discount, whichever one this order was given
        return self.__discount.apply(self.calculate_subtotal())

    def cancel(self) -> None:
        #the lines only exist as part of this order, so they are discarded with it
        self.__order_lines.clear()

    def display_order(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print("----------------------------------------")
        if not self.__order_lines:
            print("No order lines.")
        for number, order_line in enumerate(self.__order_lines, start=1):
            print(f"{number}. {order_line}")
        print("----------------------------------------")
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"Discount: {self.__discount}")
        print(f"Total: ${self.calculate_total():.2f}")
