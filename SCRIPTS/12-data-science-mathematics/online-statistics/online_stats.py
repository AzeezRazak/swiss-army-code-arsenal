# ========================================================================
# Purpose: Calculate one-pass mean and population/sample variance.
# Location: SCRIPTS/12-data-science-mathematics/online-statistics/online_stats.py
# Input/output: Finite numeric iterable; returns count, mean and variances.
# Requirements: Python 3.10+; standard library only.
# Usage (from repository root): python SCRIPTS/12-data-science-mathematics/online-statistics/online_stats.py 1 2 3 4
# Limitations: Rejects empty/nonfinite/overflowing data; floating-point rounding remains.
# ========================================================================
"""One-pass mean and population/sample variance using Welford's method."""
import argparse
import json
import math


def summarize(values):
    """Return count, mean and variances; reject empty/nonfinite/overflowing data."""
    # m2 accumulates squared deviations for the variance calculation.
    count, mean, m2 = 0, 0.0, 0.0
    for item in values:
        # Normalize one sample at a time; invalid conversions propagate.
        value = float(item)
        # NaN or infinity would invalidate all subsequent statistics.
        if not math.isfinite(value):
            raise ValueError("values must be finite")
        count += 1
        # Measure the sample against the previous running mean.
        delta = value - mean
        # Update the mean without retaining previous samples.
        mean += delta / count
        # Use old and new mean differences for Welford variance accumulation.
        m2 += delta * (value - mean)
        # Fail explicitly if finite input values overflow intermediate arithmetic.
        if not math.isfinite(mean) or not math.isfinite(m2):
            raise ValueError("floating-point range exceeded")
    if not count:
        raise ValueError("at least one value is required")
    # Divide by n for population variance; sample variance needs n > 1.
    return {"count": count, "mean": mean, "population_variance": m2 / count,
            "sample_variance": m2 / (count - 1) if count > 1 else None}


def main():
    # Define the command-line interface and built-in help output.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("values", nargs="+", type=float)
    # Parse and type-check command-line arguments before doing any work.
    args = parser.parse_args()
    try:
        print(json.dumps(summarize(args.values), allow_nan=False))
    except (ValueError, OverflowError) as error:
        parser.error(str(error))


# Run the CLI only when invoked directly, not when imported.
if __name__ == "__main__":
    main()
