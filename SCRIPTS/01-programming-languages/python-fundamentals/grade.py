# Purpose: Classify a numeric score using an explicit example grading scale.
# Location: SCRIPTS/01-programming-languages/python-fundamentals/grade.py
# Input/output: command-line values to JSON; invalid input exits 2.
# Requirements: Python 3.10+, standard library only; no installation.
# Usage from root: python SCRIPTS/01-programming-languages/python-fundamentals/grade.py 85
# Limits: educational example; see README.md for exact policies and resource limits.
"""Conditionals: Classify a numeric score using an explicit example grading scale."""
import argparse
import json
import math


def classify(score):
    """Return an example letter grade for a finite score in [0, 100]."""
    # Reject out-of-range values before comparing grade thresholds.
    score = float(score)
    if not math.isfinite(score) or not 0 <= score <= 100:
        raise ValueError("score must be finite and between 0 and 100")
    # Highest threshold first ensures each score reaches exactly one category.
    if score >= 90:
        letter = "A"
    elif score >= 80:
        letter = "B"
    elif score >= 70:
        letter = "C"
    elif score >= 60:
        letter = "D"
    else:
        letter = "F"
    return {"score": score, "grade": letter}


def main():
    # Define arguments and validate their syntax before calling the lesson function.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("score", type=float)
    args = parser.parse_args()
    try:
        # JSON keeps successful output predictable for callers and tests.
        print(json.dumps(classify(args.score), allow_nan=False, ensure_ascii=True))
    except (ValueError, OverflowError) as error:
        # argparse prints a clear diagnostic to stderr and exits with status 2.
        parser.error(str(error))


# Imports expose the reusable function without executing the command-line interface.
if __name__ == "__main__":
    main()
