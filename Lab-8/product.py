from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier) -> None:
        """initialise a Product and validate every value before storing it.

        supplier is an existing Supplier object (association): the Product keeps
        a reference to it, it does not create or own it

        raises ValueError if any value is invalid
        raises TypeError if supplier is not a Supplier object
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
        self.__supplier: Supplier = self.__validate_supplier(supplier)

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

    @staticmethod
    def __validate_supplier(supplier: Supplier) -> Supplier:
        #must be a real Supplier object, not just a supplier name or ID
        if not isinstance(supplier, Supplier):
            raise TypeError("Supplier must be a Supplier object.")
        return supplier

    # getters

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

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
        print(f"Supplier: {self.__supplier.get_name()}")

    def display_supplier_information(self) -> None:
        #the supplier prints its own details, the Product only passes the request on
        self.__supplier.display_information()

    def to_dict(self):
        #only the supplier ID is saved, the supplier itself is saved separately
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.get_supplier_id(),
        }

    def __str__(self):
        #list products
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    # abstract (every subclass must implement)

    @abstractmethod
    def get_fulfilment_info(self):
        #how the product reaches the customer, no implementation here
        pass


if __name__ == "__main__":
    #abstract: a plain Product cannot be created directly
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
    try:
        Product("P001", "Laptop", 1200.00, 15, supplier)
    except TypeError as error:
        print(f"Rejected Product(...): {error}")
