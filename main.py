#!/usr/bin/env python3
"""news-image-20261120 entrypoint.

Copies the pre-built front-page image (entry.png, drawn from code with PIL
at build time) into $MAKEFUN_OUTPUT_DIR. Standard library only: the grader
runs Python 3.13 with nothing installed, no network, 60 s. The program is
deterministic -- both runs write identical bytes.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
