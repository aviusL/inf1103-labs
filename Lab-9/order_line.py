from product import Product


class OrderLine:
    #one product and the quantity of it requested in an order.
    #part of an Order (composition): only Order.add_order_line() should create one,
    #and it is never moved to another Order.
    #it only refers to its Product (association), it does not own it

    def __init__(self, product: Product, quantity: int) -> None:
        """initialise an OrderLine.

        raises TypeError if product is not a Product object
        raises ValueError if quantity is not a whole number above zero
        """
        if not isinstance(product, Product):
            raise TypeError("An order line needs a Product object.")
        self.__product: Product = product
        self.__quantity: int = self.__validate_quantity(quantity)

    # private

    @staticmethod
    def __validate_quantity(quantity: int) -> int:
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("Quantity must be a whole number.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        return quantity

    # getters

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    # public

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def __str__(self) -> str:
        return (f"{self.__product.get_product_id()} {self.__product.get_name()} | "
                f"{self.__quantity} x ${self.__product.get_price():.2f} | "
                f"Subtotal: ${self.calculate_subtotal():.2f}")
