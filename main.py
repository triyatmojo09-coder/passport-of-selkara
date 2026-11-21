#!/usr/bin/env python3
"""Copy the Selkara passport spread (entry.png) to the output directory.

Runs with the Python 3.13 standard library only, no network.
Output directory: $MAKEFUN_OUTPUT_DIR, default /output.

Revision notes (v2):
- validates the full PNG framing (signature + IEND trailer), not just
  the signature, so a truncated asset fails loudly instead of shipping
- enforces the competition size cap (1,048,576 bytes) before writing
- writes atomically via a temporary file + os.replace, then reads the
  result back and compares SHA-256 so a partial copy can never pass
"""
import hashlib
import os
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_IEND = b"\x00\x00\x00\x00IEND\xaeB\x60\x82"
MAX_BYTES = 1_048_576


def load_entry():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("entry.png is not a PNG file (bad signature)")
    if not data.endswith(PNG_IEND):
        raise ValueError("entry.png is truncated (missing IEND chunk)")
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the {MAX_BYTES} cap")
    return data


def main():
    try:
        data = load_entry()
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    tmp = dst + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, dst)
    with open(dst, "rb") as f:
        written = f.read()
    if hashlib.sha256(written).digest() != hashlib.sha256(data).digest():
        print("error: output does not match entry.png after writing", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
