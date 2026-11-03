"""Calculate a streaming SHA-256 digest of a file."""
import argparse
import hashlib
import sys


def digest_file(path, chunk_size=1024 * 1024):
    """Return lowercase hexadecimal digest; chunk_size must be positive."""
    if not isinstance(chunk_size, int) or isinstance(chunk_size, bool) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")
    digest = hashlib.sha256()
    with open(path, "rb") as source:
        for chunk in iter(lambda: source.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args()
    try:
        print(digest_file(args.path))
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
