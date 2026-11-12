from product import Product


class Inventory:

    def __init__(self):
        # private list of Product objects
        self.__products = []

    # public

    def add_product(self, product):
        # only accepts Product objects with a unique ID
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added to the inventory.")
        if self.search_product(product.get_product_id()) is not None:
            raise ValueError(f"Product ID {product.get_product_id()} already exists.")
        self.__products.append(product)

    def search_product(self, product_id):
        # returns the matching Product (case-insensitive ID), or None if not found
        product_id = str(product_id).strip().lower()
        for product in self.__products:
            if product.get_product_id().lower() == product_id:
                return product
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("----------------------------------------")
        if not self.__products:
            print("No products available.")
        else:
            for product in self.__products:
                print(product)
        print("----------------------------------------")

    def get_products(self):
        # returns a copy so outside code cannot change the internal list
        return list(self.__products)


if __name__ == "__main__":
    inventory = Inventory()

    product1 = Product("P001", "Laptop", 1200.00, 15)
    product2 = Product("P002", "Mouse", 25.50, 40)

    inventory.add_product(product1)
    inventory.add_product(product2)
    inventory.display_all()

    found = inventory.search_product("p002")
    if found:
        print("\nProduct Found")
        found.display_information()

    print(f"\nSearch P999: {inventory.search_product('P999')}")

    try:
        inventory.add_product(Product("P001", "Duplicate", 1.00, 1))
    except ValueError as error:
        print(f"Rejected duplicate: {error}")
