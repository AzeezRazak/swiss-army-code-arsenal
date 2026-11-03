# ========================================================================
# Purpose: Find the first occurrence of a target in sorted data.
# Location: SCRIPTS/02-algorithms-data-structures/binary-search/binary_search.py
# Input/output: Sorted values and target; returns index or -1. CLI accepts integers.
# Requirements: Python 3.10+; standard library only.
# Usage (from repository root): python SCRIPTS/02-algorithms-data-structures/binary-search/binary_search.py 2 1 2 2 3
# Limitations: Library assumes sorted total-order input; CLI checks ordering.
# ========================================================================
"""First matching index in a sorted random-access sequence."""
import argparse


def first_index(values, target):
    """Return the first equal index, or -1. Requires ascending total order."""
    # Search a half-open interval; high may equal the sequence length.
    low, high = 0, len(values)
    while low < high:
        # Inspect the middle candidate to discard half of the remaining interval.
        middle = (low + high) // 2
        if values[middle] < target:
            # All candidates through middle are smaller than the target.
            low = middle + 1
        else:
            # Keep this candidate while searching left for the first duplicate.
            high = middle
    # The insertion point is a match only if it is in bounds and equal.
    return low if low < len(values) and values[low] == target else -1


def main():
    # Define the command-line interface and built-in help output.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=int)
    parser.add_argument("values", nargs="*", type=int)
    # Parse and type-check command-line arguments before doing any work.
    args = parser.parse_args()
    # Reject unsorted CLI input before applying the library precondition.
    if any(a > b for a, b in zip(args.values, args.values[1:])):
        parser.error("values must be sorted in ascending order")
    print(first_index(args.values, args.target))


# Run the CLI only when invoked directly, not when imported.
if __name__ == "__main__":
    main()
