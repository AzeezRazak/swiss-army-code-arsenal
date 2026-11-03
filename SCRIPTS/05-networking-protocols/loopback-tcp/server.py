"""Serve one bounded echo exchange on IPv4 loopback, then exit."""
import argparse
import socket
import sys
from protocol import positive_timeout, receive_frame, send_frame


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()
    try:
        timeout = positive_timeout(args.timeout)
        if not 0 <= args.port <= 65535:
            raise ValueError("port must be between 0 and 65535")
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", args.port))
            listener.listen(1)
            listener.settimeout(timeout)
            print(f"PORT {listener.getsockname()[1]}", flush=True)
            connection, _ = listener.accept()
            with connection:
                send_frame(connection, receive_frame(connection, timeout), timeout)
        return 0
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
