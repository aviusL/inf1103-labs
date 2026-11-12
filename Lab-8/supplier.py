class Supplier:
    #who supplies a product. exists on its own, it is not a part of any Product

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        """initialise a Supplier and validate every value before storing it.

        raises ValueError if any value is invalid
        """
        supplier_id = str(supplier_id).strip()
        name = str(name).strip()

        if not supplier_id:
            raise ValueError("Supplier ID cannot be empty.")
        if not name:
            raise ValueError("Supplier name cannot be empty.")

        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = self.__validate_email(contact_email)

    # private

    @staticmethod
    def __validate_email(contact_email: str) -> str:
        #basic shape check only: something@something, no spaces
        contact_email = str(contact_email).strip()
        local_part, at_sign, domain = contact_email.partition("@")
        if not at_sign or not local_part or not domain or " " in contact_email:
            raise ValueError("Contact email must look like name@example.com.")
        return contact_email

    # getters

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    # public

    def display_information(self) -> None:
        #print supplier details
        print(f"Supplier ID: {self.__supplier_id}")
        print(f"Supplier Name: {self.__name}")
        print(f"Contact Email: {self.__contact_email}")

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email,
        }

    def __str__(self) -> str:
        #list suppliers
        return (f"ID: {self.__supplier_id} | Name: {self.__name} | "
                f"Email: {self.__contact_email}")


if __name__ == "__main__":
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
    print(supplier)
    supplier.display_information()
    print(supplier.to_dict())

    for bad_email in ("", "no-at-sign", "@nodomain", "name@"):
        try:
            Supplier("S002", "Bad Email Co", bad_email)
        except ValueError as error:
            print(f"Rejected email '{bad_email}': {error}")
