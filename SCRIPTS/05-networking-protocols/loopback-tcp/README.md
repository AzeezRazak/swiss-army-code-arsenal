# Loopback TCP echo (NET-0002)

Two runnable scripts, server.py and client.py, demonstrate bounded message framing. protocol.py is a non-runnable support module. Requires Python 3.10+ standard library; no installation. Verified on Windows/Python 3.13.9 only.

## Usage

From the repository root, run in one terminal:

```powershell
python SCRIPTS/05-networking-protocols/loopback-tcp/server.py --port 8765 --timeout 30
```

It prints `PORT 8765`. Within 30 seconds, run in a second terminal:

```powershell
python SCRIPTS/05-networking-protocols/loopback-tcp/client.py 8765 hello
```

The client prints `hello`; both processes exit 0. Default server port 0 selects an available port and prints it. Both endpoints are fixed to IPv4 127.0.0.1. The server accepts exactly one connection, exchanges one frame and closes; it is intentionally not a persistent service.

## Protocol, errors and limits

A four-byte unsigned network-order length precedes at most 65,536 bytes. Empty payloads are valid. The client encodes a command-line message as UTF-8 and requires an identical echo; the server treats payloads as bytes. Oversize declarations are rejected before body allocation. Each receive has one total deadline across header and body, preventing slow-byte clients from resetting the timeout. Accept, connect and send each have their own finite timeout (default five seconds). Total process duration can span several such phases.

Invalid parameters, truncation, timeout, response mismatch and socket errors print `error:` to stderr and exit 1; argparse syntax errors exit 2. Server startup errors produce no PORT line. No retries. Memory is bounded by frame size. No encryption, authentication or external networking; other local users can connect first. Use only as a local protocol demonstration, not a production service.

## Tests

`python -m unittest discover -s TESTS -p "test_*.py" -v`

[Tests](../../../TESTS/test_sprint2.py) cover subprocess exchange, empty/max payloads, truncated header/body, oversized declarations, accept/idle deadlines, trickle-byte deadline and invalid parameters. Tests allocate ephemeral ports and clean up server processes. See [review](../../../TODO/SPRINT-0002/REVIEW.md).
