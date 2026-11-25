# SPDX-License-Identifier: MIT
"""Entry writer for the make.fun bounty 'The Excuse That Almost Works'.

The program emits a single hurried excuse line -- the kind of text a
gamer might send their boss during GTA 6 launch week -- to the fixed
harness output path.  The line is stored as three short fragments so
each clause stays easy to audit against the competition gate.
"""

import os
from pathlib import Path

# Gate limits from the official competition rules.
MAX_CHARS = 140
MIN_CHARS = 1
MAX_WORDS = 20

# The excuse, split at its natural comma boundaries.
OPENING = "Sorry, kitchen tap won't stop leaking,"
MIDDLE = " plumber's only slot is today,"
CLOSING = " downstairs has already complained twice."

DEFAULT_OUTPUT = Path("/output/entry.txt")


def build_text() -> str:
    """Assemble the excuse line from its fragments."""
    return OPENING + MIDDLE + CLOSING


def validate(text: str) -> None:
    """Raise ValueError if *text* breaks any gate limit."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(f"length {len(text)} outside {MIN_CHARS}-{MAX_CHARS}")
    if len(text.split()) > MAX_WORDS:
        raise ValueError("excuse exceeds the 20-word limit")
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line")
    if not text.strip():
        raise ValueError("excuse must not be blank")


def resolve_output() -> Path:
    """Return the output path, honouring the ENTRY_OUTPUT override."""
    override = os.environ.get("ENTRY_OUTPUT")
    return Path(override) if override else DEFAULT_OUTPUT


def verify_round_trip(target: Path, expected: bytes) -> None:
    """Read *target* back and assert it matches *expected* byte for byte.

    A harness run is only trustworthy if the file on disk is exactly
    what was validated in memory, so any mismatch (partial write,
    encoding surprise, stray newline) fails loudly instead of
    silently submitting a broken entry.
    """
    actual = target.read_bytes()
    if actual != expected:
        raise AssertionError(
            f"round-trip mismatch: wrote {len(expected)} bytes, "
            f"read back {len(actual)} bytes"
        )
    # Re-run the gate checks on the decoded on-disk content as well.
    validate(actual.decode("utf-8"))


def main() -> None:
    text = build_text()
    validate(text)
    target = resolve_output()
    target.parent.mkdir(parents=True, exist_ok=True)
    # Byte-exact write: UTF-8, no trailing newline added.
    payload = text.encode("utf-8")
    target.write_bytes(payload)
    verify_round_trip(target, payload)


if __name__ == "__main__":
    main()
