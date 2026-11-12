from product import Product


class Inventory:
    #aggregation: an Inventory groups Product objects that already exist.
    #it never creates or destroys them, removing one only drops the reference

    def __init__(self) -> None:
        #typed as the base class, so any Product subclass can be stored here
        self.__products: list[Product] = []

    # public

    def add_product(self, product: Product) -> None:
        #only accepts Product objects with a unique ID
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added to the inventory.")
        if self.find_product(product.get_product_id()) is not None:
            raise ValueError(f"Product ID {product.get_product_id()} already exists.")
        self.__products.append(product)

    def find_product(self, product_id: str) -> Product | None:
        #returns the matching Product (case-insensitive ID), or None if not found
        product_id = str(product_id).strip().lower()
        for product in self.__products:
            if product.get_product_id().lower() == product_id:
                return product
        return None

    def remove_product(self, product_id: str) -> Product | None:
        #takes the Product out of this inventory and hands it back, still usable.
        #returns None if no product has that ID
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def transfer_product(self, product_id: str, destination: "Inventory") -> bool:
        #moves the same Product object to another inventory, nothing is copied
        product = self.find_product(product_id)
        if product is None:
            return False
        destination.add_product(product)
        self.__products.remove(product)
        return True

    def contains(self, product: Product) -> bool:
        #checks for this exact object, not just a matching ID
        return any(item is product for item in self.__products)

    def count(self) -> int:
        return len(self.__products)

    def display_all(self) -> None:
        #one line per product, each product decides what its line looks like
        print("\nCurrent Inventory")
        print("----------------------------------------")
        if not self.__products:
            print("No products available.")
        else:
            for product in self.__products:
                print(product)
        print("----------------------------------------")

    def display_all_products(self) -> None:
        #full details, each Product runs its own display_information()
        for product in self.__products:
            product.display_information()
            print(product.get_fulfilment_info())
            print()

    def get_products(self) -> list[Product]:
        #returns a copy so outside code cannot change the internal list
        return list(self.__products)


if __name__ == "__main__":
    from supplier import Supplier
    from physical_product import PhysicalProduct
    from digital_product import DigitalProduct

    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.0))
    inventory.add_product(DigitalProduct("P002", "Photo Editor", 89.90, 200, supplier, 1250.0))
    inventory.display_all()

    found = inventory.find_product("p002")
    if found:
        print("\nProduct Found")
        found.display_information()

    print(f"\nFind P999: {inventory.find_product('P999')}")

    try:
        inventory.add_product(PhysicalProduct("P001", "Duplicate", 1.00, 1, supplier, 1.0))
    except ValueError as error:
        print(f"Rejected duplicate: {error}")

    removed = inventory.remove_product("P001")
    print(f"\nRemoved {removed.get_name()}, inventory now has {inventory.count()} product(s)")
