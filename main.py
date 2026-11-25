#!/usr/bin/env python3
"""Two Robots in an Elevator — make.fun bounty entry.

Writes one line of awkward small talk from one robot to another
in an elevator, to $MAKEFUN_OUTPUT_DIR/entry.txt.
Deterministic: no network, no randomness, no clock.
"""

import os
import sys

ENTRY = (
    "If this stops between floors, I am legally required to tell you "
    "my life story. It is 400 pages of error logs."
)


class LengthError(ValueError):
    """Entry length is outside the 1-200 character gate."""


class BlankError(ValueError):
    """Entry is empty or only whitespace."""


class MultiLineError(ValueError):
    """Entry contains more than one line."""


def validate(text: str) -> None:
    if not 1 <= len(text) <= 200:
        raise LengthError(
            f"entry length {len(text)} out of range 1-200 characters"
        )
    if not text.strip():
        raise BlankError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise MultiLineError("entry must be a single line")


def main() -> int:
    text = ENTRY
    validate(text)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = text.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Read-back verification: the bytes on disk must match exactly.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise IOError(
            f"read-back mismatch in {path}: "
            f"wrote {len(data)} bytes, read back {len(written)} bytes"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
