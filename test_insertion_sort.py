"""Correctness tests; run with python3 -m unittest -v."""

import itertools
from pathlib import Path
import subprocess
import sys
import unittest

from insertion_sort import insertion_sort_descending


class TaggedInteger(int):
    """An integer carrying a label so tests can observe equal-value order."""

    def __new__(cls, value, label):
        instance = super().__new__(cls, value)
        instance.label = label
        return instance


class InsertionSortTests(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(insertion_sort_descending([]), [])

    def test_single_element(self):
        self.assertEqual(insertion_sort_descending([42]), [42])

    def test_already_descending(self):
        self.assertEqual(insertion_sort_descending([9, 6, 3]), [9, 6, 3])

    def test_ascending_input(self):
        self.assertEqual(insertion_sort_descending([1, 3, 7, 9]), [9, 7, 3, 1])

    def test_all_equal(self):
        self.assertEqual(insertion_sort_descending([5, 5, 5]), [5, 5, 5])

    def test_negative_numbers(self):
        self.assertEqual(insertion_sort_descending([-8, -1, -12]), [-1, -8, -12])

    def test_mixed_values_and_duplicates(self):
        values = [28, -4, 13, 28, 0, 9, -11]
        self.assertEqual(insertion_sort_descending(values), [28, 28, 13, 9, 0, -4, -11])

    def test_modifies_and_returns_original_list(self):
        values = [2, 8, 4]
        result = insertion_sort_descending(values)
        self.assertIs(result, values)
        self.assertEqual(values, [8, 4, 2])

    def test_preserves_order_of_equal_values(self):
        values = [TaggedInteger(4, "first"), TaggedInteger(8, "high"),
                  TaggedInteger(4, "second"), TaggedInteger(4, "third")]
        result = insertion_sort_descending(values)
        self.assertEqual([item.label for item in result],
                         ["high", "first", "second", "third"])

    def test_exhaustive_small_inputs(self):
        # 1 + 3 + 9 + 27 + 81 + 243 + 729 = 1,093 different arrays.
        # sorted() is an independent test oracle, not the implementation.
        for length in range(7):
            for combination in itertools.product((-1, 0, 1), repeat=length):
                with self.subTest(values=combination):
                    actual = insertion_sort_descending(list(combination))
                    self.assertEqual(actual, sorted(combination, reverse=True))


class CommandLineTests(unittest.TestCase):
    def run_program(self, *arguments):
        program = Path(__file__).with_name("insertion_sort.py")
        return subprocess.run([sys.executable, str(program), *arguments],
                              capture_output=True, text=True, check=False)

    def test_default_example(self):
        result = self.run_program()
        self.assertEqual(result.returncode, 0)
        self.assertIn("Descending array: [28, 28, 13, 9, 0, -4, -11]", result.stdout)

    def test_custom_input(self):
        result = self.run_program("16", "-3", "8", "16", "0")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Descending array: [16, 16, 8, 0, -3]", result.stdout)

    def test_rejects_noninteger_input(self):
        result = self.run_program("12", "not-an-integer")
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid int value", result.stderr)


if __name__ == "__main__":
    unittest.main()
