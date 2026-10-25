import argparse
from typing import List


def insertion_sort_descending(values: List[int]) -> List[int]:
    """Sort values in place from largest to smallest and return the same list.

    Equal values are retained. Before each pass, the prefix to the left of
    the current position is already sorted in nonincreasing order.
    """
    for position in range(1, len(values)):
        current_value = values[position]
        scan = position - 1

        # Move smaller values right to make room for the current value.
        # Using < rather than <= preserves the relative order of equal values.
        while scan >= 0 and values[scan] < current_value:
            values[scan + 1] = values[scan]
            scan -= 1

        # scan + 1 is the position where the current value belongs.
        values[scan + 1] = current_value

    return values


def main() -> None:
    """Read optional integers, display the input, and print the sorted result."""
    parser = argparse.ArgumentParser(
        description="Sort integers in descending order using Insertion Sort."
    )
    parser.add_argument(
        "numbers", nargs="*", type=int,
        help="integers to sort; omit to run the included example",
    )
    args = parser.parse_args()
    values = args.numbers if args.numbers else [28, -4, 13, 28, 0, 9, -11]

    print("Original array:", values)
    insertion_sort_descending(values)
    print("Descending array:", values)


if __name__ == "__main__":
    main()
