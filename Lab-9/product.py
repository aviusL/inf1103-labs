import math
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

        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = self.__validate_price(price)
        self.__stock: int = self.__validate_stock(stock)
        self.__supplier: Supplier = self.__validate_supplier(supplier)

    # private

    #validation rules live here in Product, so every subclass gets the same ones (LSP)

    @staticmethod
    def __validate_price(price: float) -> float:
        #True/False would quietly become 1.0/0.0, so reject them outright
        if isinstance(price, bool):
            raise ValueError("Price must be a number.")
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValueError("Price must be a number.") from None
        #nan and inf are floats but not prices
        if not math.isfinite(price) or price <= 0:
            raise ValueError("Price must be greater than zero.")
        return price

    @staticmethod
    def __validate_stock(stock: int) -> int:
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

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    # public

    def update_stock(self, quantity: int) -> None:
        """set the stock level to a new quantity.

        contract every subclass keeps (LSP): any whole number >= 0 is accepted
        and becomes the new stock level, anything else raises ValueError.
        for a DigitalProduct the stock is the number of licences available.
        """

        self.__stock = self.__validate_stock(quantity)

    def display_information(self) -> None:
        #print product details
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(f"Supplier: {self.__supplier.get_name()}")

    def display_supplier_information(self) -> None:
        #the supplier prints its own details, the Product only passes the request on
        self.__supplier.display_information()

    def to_dict(self) -> dict[str, str | float | int]:
        #only the supplier ID is saved, the supplier itself is saved separately
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.get_supplier_id(),
        }

    def __str__(self) -> str:
        #list products
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    # abstract (every subclass must implement)

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        #how the product reaches the customer, every subclass returns a description
        pass


if __name__ == "__main__":
    #abstract: a plain Product cannot be created directly
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
    try:
        Product("P001", "Laptop", 1200.00, 15, supplier)
    except TypeError as error:
        print(f"Rejected Product(...): {error}")
