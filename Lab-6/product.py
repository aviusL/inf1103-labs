
class Product:

    def __init__(self, product_id, name, price, stock):
        """initialise a Product and validate every value before storing it.

        raises ValueError if any value is invalid
        """
        product_id = str(product_id).strip()
        name = str(name).strip()

        if not product_id:
            raise ValueError("Product ID cannot be empty.")
        if not name:
            raise ValueError("Product name cannot be empty.")

        self.__product_id = product_id
        self.__name = name
        self.__price = self.__validate_price(price)
        self.__stock = self.__validate_stock(stock)

    # private

    @staticmethod
    def __validate_price(price):
        price = float(price)
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        return price

    @staticmethod
    def __validate_stock(stock):
        if isinstance(stock, bool) or not isinstance(stock, int):
            raise ValueError("Stock quantity must be a whole number.")
        if stock < 0:
            raise ValueError("Stock quantity cannot be negative.")
        return stock

    # getters

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    # public

    def update_stock(self, quantity):
        #set the stock level to a new quantity.

        self.__stock = self.__validate_stock(quantity)

    def display_information(self):
        #print product details
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    def __str__(self):
        #list products
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")


if __name__ == "__main__":
    laptop = Product("P001", "Laptop", 1200.00, 15)
    print(laptop)

    laptop.update_stock(20)
    laptop.display_information()

    try:
        laptop.update_stock(-5)
    except ValueError as error:
        print(f"Rejected update_stock(-5): {error}")

    # Encapsulation:
    laptop.__stock = 999
    print(f"After 'laptop.__stock = 999', get_stock() still returns {laptop.get_stock()}")
