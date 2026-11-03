"""Send one UTF-8 message to a loopback echo server."""
import argparse
import socket
import sys
from protocol import MAX_PAYLOAD, positive_timeout, receive_frame, send_frame


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("port", type=int)
    parser.add_argument("message")
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()
    try:
        timeout = positive_timeout(args.timeout)
        if not 1 <= args.port <= 65535:
            raise ValueError("port must be between 1 and 65535")
        payload = args.message.encode("utf-8")
        if len(payload) > MAX_PAYLOAD:
            raise ValueError("payload exceeds 65536 bytes")
        with socket.create_connection(("127.0.0.1", args.port), timeout=timeout) as connection:
            send_frame(connection, payload, timeout)
            reply = receive_frame(connection, timeout)
        if reply != payload:
            raise ValueError("echo response differs from request")
        print(reply.decode("utf-8"))
        return 0
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
