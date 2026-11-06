# Purpose: Calculate distance and midpoint for two finite 2D coordinates.
# Location: SCRIPTS/01-programming-languages/python-fundamentals-2/tuple_coordinates.py
# Input/output: four numeric coordinates to a JSON object; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; no installation.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals-2/tuple_coordinates.py 0 0 3 4
# Limits: coordinates must convert to finite floats; results must remain finite.
"""Tuples: unpack and measure two finite two-dimensional coordinates."""
import argparse
import json
import math
import numbers


def _point(value, label):
    if isinstance(value, (str, bytes)):
        raise ValueError(f"{label} must contain exactly two numbers")
    try:
        values = tuple(value)
    except TypeError as error:
        raise ValueError(f"{label} must contain exactly two numbers") from error
    if len(values) != 2:
        raise ValueError(f"{label} must contain exactly two numbers")
    converted = []
    for coordinate in values:
        if isinstance(coordinate, bool) or not isinstance(coordinate, numbers.Real):
            raise ValueError("coordinates must be real numbers")
        try:
            number = float(coordinate)
        except (OverflowError, ValueError) as error:
            raise ValueError("coordinates must fit in finite floats") from error
        if not math.isfinite(number):
            raise ValueError("coordinates must be finite")
        converted.append(number)
    return tuple(converted)


def measure(first, second):
    """Return Euclidean distance and midpoint for two validated points."""
    x1, y1 = _point(first, "first")
    x2, y2 = _point(second, "second")
    distance = math.hypot(x2 - x1, y2 - y1)
    midpoint = ((x1 + x2) / 2, (y1 + y2) / 2)
    if not math.isfinite(distance) or not all(math.isfinite(value) for value in midpoint):
        raise ValueError("distance and midpoint must be finite")
    return {"distance": distance, "midpoint": list(midpoint)}


def main():
    # Four arguments make the two tuple unpacking operations visible at the CLI boundary.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("coordinates", nargs=4, type=float, metavar="NUMBER")
    args = parser.parse_args()
    try:
        values = args.coordinates
        print(json.dumps(measure(values[:2], values[2:]), allow_nan=False))
    except (ValueError, OverflowError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
