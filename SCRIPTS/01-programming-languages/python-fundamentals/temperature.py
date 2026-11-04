# Purpose: Convert Celsius to Fahrenheit.
# Location: SCRIPTS/01-programming-languages/python-fundamentals/temperature.py
# Input/output: command-line values to JSON; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; no installation.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals/temperature.py 0
# Limits: educational example; see README.md for exact policies and resource limits.
"""Variables and arithmetic: Convert Celsius to Fahrenheit."""
import argparse
import json
import math


def convert(celsius):
    """Return Celsius/Fahrenheit values; reject nonfinite or overflowing input."""
    # Converting to float demonstrates a numeric type conversion.
    celsius = float(celsius)
    if not math.isfinite(celsius):
        raise ValueError("temperature must be finite")
    # Apply the scale factor before the offset using ordinary arithmetic.
    fahrenheit = celsius * 1.8 + 32
    if not math.isfinite(fahrenheit):
        raise ValueError("converted temperature exceeds floating-point range")
    return {"celsius": celsius, "fahrenheit": fahrenheit}


def main():
    # Define arguments and validate their syntax before calling the lesson function.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("celsius", type=float)
    args = parser.parse_args()
    try:
        # JSON keeps successful output predictable for callers and tests.
        print(json.dumps(convert(args.celsius), allow_nan=False, ensure_ascii=True))
    except (ValueError, OverflowError) as error:
        # argparse prints a clear diagnostic to stderr and exits with status 2.
        parser.error(str(error))


# Imports expose the reusable function without executing the command-line interface.
if __name__ == "__main__":
    main()
