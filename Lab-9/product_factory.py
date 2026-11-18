from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


class ProductFactory:
    #factory pattern: the one place that decides which Product subclass to build.
    #the rest of the program asks for a Product and never names a subclass.
    #it creates products but does not keep them (a dependency, not an association).
    #a new product type still means a change here, so the factory itself breaks OCP;
    #that one change is accepted to keep a small program simple

    #used when the source gives none, e.g. products.csv or an old inventory.json
    DEFAULT_WEIGHT: float = 1.0
    DEFAULT_DOWNLOAD_SIZE: float = 100.0

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               weight: float | None = None, download_size: float | None = None) -> Product:
        """build the Product subclass named by product_type: "physical" or "digital".

        weight is only used for physical products, download_size only for digital ones

        raises ValueError for an unknown product type, or if the product rejects a value
        """
        kind = str(product_type).strip().lower()

        if kind == "physical":
            if weight is None:
                weight = ProductFactory.DEFAULT_WEIGHT
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, weight)
        if kind == "digital":
            if download_size is None:
                download_size = ProductFactory.DEFAULT_DOWNLOAD_SIZE
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, download_size)

        raise ValueError(f"Unknown product type: {product_type}")
