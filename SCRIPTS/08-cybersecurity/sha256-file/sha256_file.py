# ========================================================================
# Purpose: Compute a SHA-256 digest with bounded read buffers.
# Location: SCRIPTS/08-cybersecurity/sha256-file/sha256_file.py
# Input/output: Stable file path; outputs hexadecimal digest.
# Requirements: Python 3.10+; standard library only.
# Usage (from repository root): python SCRIPTS/08-cybersecurity/sha256-file/sha256_file.py EXAMPLES/abc.txt
# Limitations: A hash does not authenticate a sender; concurrent writes are not detected.
# ========================================================================
"""Calculate a streaming SHA-256 digest of a file."""
import argparse
import hashlib
import hmac
import re
import sys


def digest_file(path, chunk_size=1024 * 1024):
    """Return lowercase hexadecimal digest; chunk_size must be positive."""
    if not isinstance(chunk_size, int) or isinstance(chunk_size, bool) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")
    # Initialize incremental hashing without loading the whole file.
    digest = hashlib.sha256()
    with open(path, "rb") as source:
        # Read bounded chunks until the empty-byte EOF sentinel.
        for chunk in iter(lambda: source.read(chunk_size), b""):
            # Extend the digest with this chunk in file order.
            digest.update(chunk)
    # Expose the final digest in the conventional lowercase hexadecimal form.
    return digest.hexdigest()


def expected_digest(value):
    """Accept exactly 64 ASCII hexadecimal characters and normalize case."""
    if re.fullmatch(r"[0-9a-fA-F]{64}", value) is None:
        raise argparse.ArgumentTypeError("expected digest must contain exactly 64 hexadecimal characters")
    return value.lower()


def main():
    # Define the command-line interface and built-in help output.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--check", type=expected_digest, metavar="SHA256",
                        help="compare against an expected SHA-256 digest")
    # Parse and type-check command-line arguments before doing any work.
    args = parser.parse_args()
    try:
        actual = digest_file(args.path)
        if args.check is None:
            # Preserve the original digest-only output when verification is not requested.
            print(actual)
        elif hmac.compare_digest(actual, args.check):
            print("OK")
        else:
            # A mismatch is an unsuccessful check; leave stdout empty for automation.
            print("error: SHA-256 mismatch", file=sys.stderr)
            return 1
    except OSError as error:
        # Keep diagnostics off stdout so successful output stays machine-readable.
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


# Run the CLI only when invoked directly, not when imported.
if __name__ == "__main__":
    sys.exit(main())
