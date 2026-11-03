"""First matching index in a sorted random-access sequence."""
import argparse


def first_index(values, target):
    """Return the first equal index, or -1. Requires ascending total order."""
    low, high = 0, len(values)
    while low < high:
        middle = (low + high) // 2
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle
    return low if low < len(values) and values[low] == target else -1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=int)
    parser.add_argument("values", nargs="*", type=int)
    args = parser.parse_args()
    if any(a > b for a, b in zip(args.values, args.values[1:])):
        parser.error("values must be sorted in ascending order")
    print(first_index(args.values, args.target))


if __name__ == "__main__":
    main()
