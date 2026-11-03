"""One-pass mean and population/sample variance using Welford's method."""
import argparse
import json
import math


def summarize(values):
    """Return count, mean and variances; reject empty/nonfinite/overflowing data."""
    count, mean, m2 = 0, 0.0, 0.0
    for item in values:
        value = float(item)
        if not math.isfinite(value):
            raise ValueError("values must be finite")
        count += 1
        delta = value - mean
        mean += delta / count
        m2 += delta * (value - mean)
        if not math.isfinite(mean) or not math.isfinite(m2):
            raise ValueError("floating-point range exceeded")
    if not count:
        raise ValueError("at least one value is required")
    return {"count": count, "mean": mean, "population_variance": m2 / count,
            "sample_variance": m2 / (count - 1) if count > 1 else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("values", nargs="+", type=float)
    args = parser.parse_args()
    try:
        print(json.dumps(summarize(args.values), allow_nan=False))
    except (ValueError, OverflowError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
