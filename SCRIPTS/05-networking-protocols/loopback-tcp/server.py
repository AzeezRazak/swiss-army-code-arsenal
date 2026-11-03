# ========================================================================
# Purpose: Serve one framed echo request on IPv4 loopback, then exit.
# Location: SCRIPTS/05-networking-protocols/loopback-tcp/server.py
# Input/output: Optional port/timeout; prints selected port and echoes bytes to client.
# Requirements: Python 3.10+; standard library only.
# Usage (from repository root): python SCRIPTS/05-networking-protocols/loopback-tcp/server.py --port 8765 --timeout 30
# Limitations: One client only; bounded frame and timeouts; no authentication.
# ========================================================================
"""Serve one bounded echo exchange on IPv4 loopback, then exit."""
import argparse
import socket
import sys
from protocol import positive_timeout, receive_frame, send_frame


def main():
    # Define the command-line interface and built-in help output.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=5.0)
    # Parse and type-check command-line arguments before doing any work.
    args = parser.parse_args()
    try:
        timeout = positive_timeout(args.timeout)
        if not 0 <= args.port <= 65535:
            raise ValueError("port must be between 0 and 65535")
        with socket.socket() as listener:
            # Keep the service on this machine; port zero requests an available port.
            listener.bind(("127.0.0.1", args.port))
            # This example serves a single accepted connection, then exits.
            listener.listen(1)
            listener.settimeout(timeout)
            # Flush the actual port immediately so callers can discover readiness.
            print(f"PORT {listener.getsockname()[1]}", flush=True)
            # Wait only up to the configured timeout for the first local client.
            connection, _ = listener.accept()
            # Commit the whole batch on success, or roll it back on an exception.
            with connection:
                # Echo one validated frame; the context manager then closes the socket.
                send_frame(connection, receive_frame(connection, timeout), timeout)
        return 0
    except (OSError, ValueError) as error:
        # Keep diagnostics off stdout so successful output stays machine-readable.
        print(f"error: {error}", file=sys.stderr)
        return 1


# Run the CLI only when invoked directly, not when imported.
if __name__ == "__main__":
    sys.exit(main())
