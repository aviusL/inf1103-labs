from discount_strategy import PercentageDiscount


class StudentDiscount(PercentageDiscount):
    #lab 9 section 2.4: a fourth strategy added in its own file.
    #Order and the other strategies were not edited to add it.
    #it reuses PercentageDiscount's maths, only the rate is fixed

    STUDENT_PERCENTAGE: float = 5.0

    def __init__(self) -> None:
        super().__init__(self.STUDENT_PERCENTAGE)

    def __str__(self) -> str:
        return f"Student discount ({self.get_percentage():g}% off)"
