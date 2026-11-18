#runs the lab 8 relationship scripts as automated tests.
#each script ends in assert statements, so it passes only if main() finishes
#without an AssertionError. their printed walkthrough is hidden here; to see it,
#run one directly, e.g. python -m tests.test_association

import io
import unittest
from contextlib import redirect_stdout

from tests import test_aggregation, test_association, test_composition, test_lsp_polymorphism


class Lab8RelationshipTests(unittest.TestCase):

    def run_script(self, script) -> None:
        with redirect_stdout(io.StringIO()):
            script.main()

    def test_association_supplier_and_product(self) -> None:
        self.run_script(test_association)

    def test_aggregation_inventory_and_product(self) -> None:
        self.run_script(test_aggregation)

    def test_composition_order_and_order_line(self) -> None:
        self.run_script(test_composition)

    def test_lsp_and_polymorphism_through_product(self) -> None:
        self.run_script(test_lsp_polymorphism)


if __name__ == "__main__":
    unittest.main()
