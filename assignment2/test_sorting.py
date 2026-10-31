"""Correctness, stability, and stack-safety checks for both implementations."""

import itertools
import random
import unittest
from dataclasses import dataclass

from sorting import merge_sort, quick_sort


@dataclass
class Record:
    key: int
    label: str

    def __le__(self, other: "Record") -> bool:
        return self.key <= other.key


class SortingTests(unittest.TestCase):
    def check_both(self, original):
        expected = sorted(original)
        for algorithm in (merge_sort, quick_sort):
            with self.subTest(algorithm=algorithm.__name__, input=original):
                actual = original.copy()
                self.assertIs(algorithm(actual), actual)
                self.assertEqual(actual, expected)

    def test_edge_cases(self):
        for values in ([], [7], [2, 1], [1, 2], [5] * 40,
                       [-4, 0, 3, -4, 2], [1.5, -2.3, 1.5],
                       ["pear", "apple", "orange", "apple"]):
            self.check_both(values)

    def test_exhaustive_small_arrays(self):
        # All 1,093 arrays of lengths zero through six over three values.
        for size in range(7):
            for values in itertools.product((-1, 0, 1), repeat=size):
                self.check_both(list(values))

    def test_every_permutation_of_seven_values(self):
        for values in itertools.permutations(range(7)):
            self.check_both(list(values))

    def test_seeded_inputs_and_duplicates(self):
        rng = random.Random(532)
        for size in (17, 127, 1000):
            self.check_both(rng.sample(range(size * 5), size))
            self.check_both([rng.randrange(-8, 9) for _ in range(size)])

    def test_merge_sort_preserves_tie_order(self):
        values = [Record(2, "a"), Record(1, "b"), Record(2, "c"),
                  Record(1, "d"), Record(2, "e")]
        merge_sort(values)
        self.assertEqual([r.label for r in values], ["b", "d", "a", "c", "e"])

    def test_quick_sort_handles_degenerate_partitions(self):
        # These exceed the usual Python recursion limit without changing it.
        for values in (list(range(3000)), list(range(2999, -1, -1)), [1] * 3000):
            self.check_both(values)


if __name__ == "__main__":
    unittest.main()
