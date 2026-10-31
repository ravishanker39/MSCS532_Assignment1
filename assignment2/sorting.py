"""Divide-and-conquer sorts that modify a list and return the same list."""

from typing import TypeVar

T = TypeVar("T")


def merge_sort(values: list[T]) -> list[T]:
    """Stable ascending sort; Theta(n log n) time and Theta(n) extra space.

    A single reusable buffer avoids allocating sliced sublists at each level.
    Elements must support <= consistently; comparisons are assumed O(1).
    """
    if len(values) < 2:
        return values
    buffer = values.copy()

    def sort_range(lo: int, hi: int) -> None:
        # Half-open ranges make the empty and one-element base cases explicit.
        if hi - lo < 2:
            return
        mid = (lo + hi) // 2
        sort_range(lo, mid)
        sort_range(mid, hi)
        left, right = lo, mid
        for target in range(lo, hi):
            # Taking the left item on equality preserves the original tie order.
            if left < mid and (right >= hi or values[left] <= values[right]):
                buffer[target] = values[left]
                left += 1
            else:
                buffer[target] = values[right]
                right += 1
        for target in range(lo, hi):
            values[target] = buffer[target]

    sort_range(0, len(values))
    return values


def quick_sort(values: list[T]) -> list[T]:
    """Ascending Lomuto quicksort with a last-element pivot; not stable.

    Expected time on uniform random permutations is Theta(n log n), but
    monotone or all-equal input takes Theta(n squared). Recursing only into
    the smaller side bounds auxiliary stack space by O(log n) in every case.
    """
    def partition(lo: int, hi: int) -> int:
        pivot = values[hi]
        boundary = lo
        for index in range(lo, hi):
            if values[index] <= pivot:
                values[boundary], values[index] = values[index], values[boundary]
                boundary += 1
        values[boundary], values[hi] = values[hi], values[boundary]
        return boundary

    def sort_range(lo: int, hi: int) -> None:
        while lo < hi:
            pivot_index = partition(lo, hi)
            # Each recursive child has at most half as many remaining elements.
            # Iteration handles the larger side without growing the call stack.
            if pivot_index - lo < hi - pivot_index:
                sort_range(lo, pivot_index - 1)
                lo = pivot_index + 1
            else:
                sort_range(pivot_index + 1, hi)
                hi = pivot_index - 1

    sort_range(0, len(values) - 1)
    return values


if __name__ == "__main__":
    sample = [18, 4, 12, 4, -3, 9]
    print("Input:     ", sample)
    print("Merge sort:", merge_sort(sample.copy()))
    print("Quick sort:", quick_sort(sample.copy()))
