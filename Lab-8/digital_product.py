from product import Product
from supplier import Supplier
from can_be_shipped import CanBeShipped


class DigitalProduct(Product):
    #inherits from Product only, does NOT implement CanBeShipped

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float) -> None:
        """initialise a DigitalProduct, reusing the Product constructor.

        raises ValueError if download_size is invalid
        """
        #the Supplier is passed up, Product stores the reference
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = self.__validate_download_size(download_size)

    # private

    @staticmethod
    def __validate_download_size(download_size: float) -> float:
        download_size = float(download_size)
        if download_size <= 0:
            raise ValueError("Download size must be greater than zero.")
        return download_size

    # getters

    def get_download_size(self) -> float:
        return self.__download_size

    # public (overrides Product)

    def display_information(self) -> None:
        #parent prints the common details, child adds download size
        super().display_information()
        print(f"Download Size: {self.__download_size:.2f} MB")

    def to_dict(self) -> dict[str, str | float | int]:
        #parent dict plus product type and download size
        return {"type": "digital", **super().to_dict(), "download_size": self.__download_size}

    def __str__(self) -> str:
        #list products
        return f"{super().__str__()} | Download Size: {self.__download_size:.2f} MB"

    # abstract method from Product

    def get_fulfilment_info(self) -> str:
        return "Digital product: delivered by download, no shipping required."


if __name__ == "__main__":
    supplier = Supplier("S003", "SoftWorks", "licensing@softworks.example")

    os_product = DigitalProduct("P020", "Operating System", 199.00, 100, supplier, 4500)
    print(os_product)
    os_product.display_information()
    print(f"Operating System is-a Product: {isinstance(os_product, Product)}")
    print(f"Operating System can-be-shipped: {isinstance(os_product, CanBeShipped)}")
    print(os_product.get_fulfilment_info())
    print(os_product.to_dict())

    try:
        DigitalProduct("P021", "Empty File", 1.00, 1, supplier, -10)
    except ValueError as error:
        print(f"Rejected download size -10: {error}")
