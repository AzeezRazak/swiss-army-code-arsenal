# ========================================================================
# Purpose: Share bounded binary framing between server and client.
# Location: SCRIPTS/05-networking-protocols/loopback-tcp/protocol.py
# Input/output: Connected socket and bytes; sends or receives length-prefixed payloads.
# Requirements: Python 3.10+; standard library only.
# Usage (from repository root): Import from client.py or server.py; this is not a runnable script.
# Limitations: One absolute receive deadline per frame; maximum payload 65536 bytes.
# ========================================================================
"""Bounded binary framing shared by the loopback demonstration."""
import math
import socket
import struct
import time

# Reject larger frames before allocating or reading their bodies.
MAX_PAYLOAD = 65536


def positive_timeout(value):
    value = float(value)
    # Prevent infinite, NaN or nonpositive socket timeouts.
    if not math.isfinite(value) or value <= 0:
        raise ValueError("timeout must be positive and finite")
    return value


def receive_exact(connection, size, deadline):
    chunks = bytearray()
    while len(chunks) < size:
        # Use elapsed monotonic time so trickled bytes cannot reset the deadline.
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("frame deadline exceeded")
        connection.settimeout(remaining)
        # TCP can return fewer bytes than requested; keep assembling the frame.
        chunk = connection.recv(size - len(chunks))
        # EOF before the expected length means the peer truncated the frame.
        if not chunk:
            raise ValueError("truncated frame")
        chunks.extend(chunk)
    return bytes(chunks)


def receive_frame(connection, timeout):
    # Share one deadline between the header and body reads.
    deadline = time.monotonic() + positive_timeout(timeout)
    # Decode a four-byte unsigned length in network (big-endian) order.
    size = struct.unpack("!I", receive_exact(connection, 4, deadline))[0]
    if size > MAX_PAYLOAD:
        raise ValueError("payload exceeds 65536 bytes")
    return receive_exact(connection, size, deadline)


def send_frame(connection, payload, timeout):
    if len(payload) > MAX_PAYLOAD:
        raise ValueError("payload exceeds 65536 bytes")
    connection.settimeout(positive_timeout(timeout))
    # Send the length prefix and body completely, subject to the send timeout.
    connection.sendall(struct.pack("!I", len(payload)) + payload)
