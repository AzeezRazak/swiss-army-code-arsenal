"""Bounded binary framing shared by the loopback demonstration."""
import math
import socket
import struct
import time

MAX_PAYLOAD = 65536


def positive_timeout(value):
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError("timeout must be positive and finite")
    return value


def receive_exact(connection, size, deadline):
    chunks = bytearray()
    while len(chunks) < size:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("frame deadline exceeded")
        connection.settimeout(remaining)
        chunk = connection.recv(size - len(chunks))
        if not chunk:
            raise ValueError("truncated frame")
        chunks.extend(chunk)
    return bytes(chunks)


def receive_frame(connection, timeout):
    deadline = time.monotonic() + positive_timeout(timeout)
    size = struct.unpack("!I", receive_exact(connection, 4, deadline))[0]
    if size > MAX_PAYLOAD:
        raise ValueError("payload exceeds 65536 bytes")
    return receive_exact(connection, size, deadline)


def send_frame(connection, payload, timeout):
    if len(payload) > MAX_PAYLOAD:
        raise ValueError("payload exceeds 65536 bytes")
    connection.settimeout(positive_timeout(timeout))
    connection.sendall(struct.pack("!I", len(payload)) + payload)
