# Purpose: Build an offline request-budget schedule for a bounded scanner run.
# Location: SCRIPTS/09-automation-scripting/request-budget-plan/build_rate_plan.py
# Input/output: request count and limits to JSON batches; never sends requests.
# Requirements: Python 3.10+, standard library only; no network or background process.
# Usage from root: python SCRIPTS/09-automation-scripting/request-budget-plan/build_rate_plan.py --requests 5 --interval 2 --concurrency 2 --body-bytes 4096
# Limits: at most 10,000 requests, concurrency 1-20 and body size 1-1 MiB.
"""Create a deterministic schedule that a separately authorized runner could review."""
import argparse
import json
import math

MAX_REQUESTS = 10_000


def build_plan(requests, interval, concurrency, body_bytes):
    """Return numbered batches and total planned duration without performing I/O."""
    if not isinstance(requests, int) or not 1 <= requests <= MAX_REQUESTS:
        raise ValueError(f"requests must be 1-{MAX_REQUESTS}")
    if not isinstance(interval, (int, float)) or isinstance(interval, bool) or not 0 <= interval <= 3600:
        raise ValueError("interval must be between 0 and 3600 seconds")
    if not isinstance(concurrency, int) or not 1 <= concurrency <= 20:
        raise ValueError("concurrency must be 1-20")
    if not isinstance(body_bytes, int) or not 1 <= body_bytes <= 1_048_576:
        raise ValueError("body_bytes must be 1-1048576")
    batches = [{"batch": number, "requests": min(concurrency, requests - (number - 1) * concurrency), "wait_seconds": (number - 1) * interval} for number in range(1, math.ceil(requests / concurrency) + 1)]
    return {"requests": requests, "concurrency": concurrency, "body_bytes": body_bytes, "interval_seconds": interval, "batches": batches, "duration_seconds": (len(batches) - 1) * interval}


def main():
    # Emit a plan only; no transport library or socket is imported by this utility.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requests", type=int, required=True)
    parser.add_argument("--interval", type=float, required=True)
    parser.add_argument("--concurrency", type=int, required=True)
    parser.add_argument("--body-bytes", type=int, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(build_plan(args.requests, args.interval, args.concurrency, args.body_bytes), ensure_ascii=True))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
