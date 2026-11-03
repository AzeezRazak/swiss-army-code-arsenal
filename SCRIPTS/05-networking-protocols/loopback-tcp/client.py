# ========================================================================
# Purpose: Send one UTF-8 request to the local framed echo server.
# Location: SCRIPTS/05-networking-protocols/loopback-tcp/client.py
# Input/output: Loopback port and message; outputs the identical echoed message.
# Requirements: Python 3.10+; standard library only.
# Usage (from repository root): python SCRIPTS/05-networking-protocols/loopback-tcp/client.py 8765 hello
# Limitations: Loopback only; 65536-byte maximum; finite phase timeouts; no authentication.
# ========================================================================
"""Send one UTF-8 message to a loopback echo server."""
import argparse
import socket
import sys
from protocol import MAX_PAYLOAD, positive_timeout, receive_frame, send_frame


def main():
    # Define the command-line interface and built-in help output.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("port", type=int)
    parser.add_argument("message")
    parser.add_argument("--timeout", type=float, default=5.0)
    # Parse and type-check command-line arguments before doing any work.
    args = parser.parse_args()
    try:
        timeout = positive_timeout(args.timeout)
        if not 1 <= args.port <= 65535:
            raise ValueError("port must be between 1 and 65535")
        # Measure payload limits in encoded bytes, not character count.
        payload = args.message.encode("utf-8")
        if len(payload) > MAX_PAYLOAD:
            raise ValueError("payload exceeds 65536 bytes")
        with socket.create_connection(("127.0.0.1", args.port), timeout=timeout) as connection:
            send_frame(connection, payload, timeout)
            reply = receive_frame(connection, timeout)
        # Treat a different response as a protocol error, not a successful echo.
        if reply != payload:
            raise ValueError("echo response differs from request")
        print(reply.decode("utf-8"))
        return 0
    except (OSError, ValueError) as error:
        # Keep diagnostics off stdout so successful output stays machine-readable.
        print(f"error: {error}", file=sys.stderr)
        return 1


# Run the CLI only when invoked directly, not when imported.
if __name__ == "__main__":
    sys.exit(main())
