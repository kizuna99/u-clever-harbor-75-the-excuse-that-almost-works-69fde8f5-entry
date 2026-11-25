# SPDX-License-Identifier: MIT
"""Write the winning excuse line to /output/entry.txt.

Winner of a 16-candidate criteria-ordered tournament plus 4 refinement
iterations (see builder notes): a live, boring, specific domestic emergency
(kitchen tap leak, plumber's only slot today) with third-party pressure
(downstairs has already complained twice) — the humour comes from the
detail itself, in a hurried one-line text voice, with no banned trope
(no fever, flat tyre or grandmother) and no game confession.
16 words, inside the 1-140 character gate.
"""
import os

TEXT = "Sorry, kitchen tap won't stop leaking, plumber's only slot is today, downstairs has already complained twice."


def main() -> None:
    out = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write(TEXT)


if __name__ == "__main__":
    main()
