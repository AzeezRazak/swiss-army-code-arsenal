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


def main():
    # Define the command-line interface and built-in help output.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    # Parse and type-check command-line arguments before doing any work.
    args = parser.parse_args()
    try:
        print(digest_file(args.path))
    except OSError as error:
        # Keep diagnostics off stdout so successful output stays machine-readable.
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


# Run the CLI only when invoked directly, not when imported.
if __name__ == "__main__":
    sys.exit(main())
