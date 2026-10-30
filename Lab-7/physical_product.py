from product import Product


class PhysicalProduct(Product):

    def __init__(self, product_id, name, price, stock, weight):
        """initialise a PhysicalProduct, reusing the Product constructor.

        raises ValueError if weight is invalid
        """
        super().__init__(product_id, name, price, stock)
        self.__weight = self.__validate_weight(weight)

    # private

    @staticmethod
    def __validate_weight(weight):
        weight = float(weight)
        if weight <= 0:
            raise ValueError("Weight must be greater than zero.")
        return weight

    # getters

    def get_weight(self):
        return self.__weight

    # public (overrides Product)

    def display_information(self):
        #parent prints the common details, child adds weight
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")

    def to_dict(self):
        #parent dict plus product type and weight
        return {"type": "physical", **super().to_dict(), "weight": self.__weight}

    def __str__(self):
        #list products
        return f"{super().__str__()} | Weight: {self.__weight:.2f} kg"


if __name__ == "__main__":
    guitar = PhysicalProduct("P010", "Guitar", 350.00, 5, 3.5)
    print(guitar)
    guitar.display_information()

    #inherited from Product without rewriting it
    guitar.update_stock(8)
    print(f"Stock after update_stock(8): {guitar.get_stock()}")
    print(f"Guitar is-a Product: {isinstance(guitar, Product)}")
    print(guitar.to_dict())

    try:
        PhysicalProduct("P011", "Feather", 1.00, 1, 0)
    except ValueError as error:
        print(f"Rejected weight 0: {error}")
