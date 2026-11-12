#runs every lab 8 test in order and stops at the first failure
#run with: python run_tests.py

import test_association
import test_aggregation
import test_composition
import test_lsp_polymorphism

TESTS = [
    ("Section 2 - Association", test_association),
    ("Section 3 - Aggregation", test_aggregation),
    ("Section 4 - Composition", test_composition),
    ("Sections 6 and 7 - LSP and Polymorphism", test_lsp_polymorphism),
]


def main() -> None:
    for title, module in TESTS:
        print("\n" + "=" * 50)
        print(title)
        print("=" * 50)
        module.main()

    print("\n" + "=" * 50)
    print(f"All {len(TESTS)} test files passed.")
    print("=" * 50)


if __name__ == "__main__":
    main()
