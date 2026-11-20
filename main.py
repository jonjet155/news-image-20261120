#!/usr/bin/env python3
"""Ship the 20 November 2026 front page for make.fun news-image-20261120.

The front page is a finished picture that lives beside this file as
entry.png. This program does exactly one thing: it puts a byte-identical
copy of that picture where the bounty harness looks for it.

Why a copy instead of drawing here: the grader runs with the standard
library only, no network, one CPU, 512 MB and 60 seconds. The picture
was drawn beforehand (see build_entry.py in this repository), so this
program needs nothing beyond the standard library and always produces
the same bytes.

Where the copy goes: MAKEFUN_OUTPUT_DIR when set, else OUTPUT_DIR when
set, else /output. The destination directory is created if missing.
Before writing, the bundled picture is sanity-checked (a real PNG or
JPEG, at most 1024 on a side, at most 1 MiB). After writing, the copy
is hashed and compared with the original, so a short write fails loudly
instead of silently shipping a broken file.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PICTURE = HERE / "entry.png"
BYTE_LIMIT = 1_048_576
EDGE_LIMIT = 1024

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def png_dimensions(data):
    """(width, height) if data is a PNG, else None."""
    if data[:8] != PNG_MAGIC or data[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", data[16:24])


def jpeg_dimensions(data):
    """(width, height) if data is a JPEG, else None."""
    if data[:3] != JPEG_MAGIC:
        return None
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            return None
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", data[i + 5:i + 9])
            return width, height
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
        else:
            (length,) = struct.unpack(">H", data[i + 2:i + 4])
            if length < 2:
                return None  # a segment shorter than its own length field
            i += 2 + length
    return None


def fail(message):
    print(f"main.py: {message}", file=sys.stderr)
    return 1


def run():
    out_dir = Path(
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return fail(f"cannot make output directory {out_dir}: {exc}")

    try:
        data = PICTURE.read_bytes()
    except OSError as exc:
        return fail(f"cannot read {PICTURE}: {exc}")

    dims = png_dimensions(data) or jpeg_dimensions(data)
    if dims is None:
        return fail("entry.png is not a readable PNG or JPEG")
    width, height = dims
    if width > EDGE_LIMIT or height > EDGE_LIMIT:
        return fail(f"entry.png is {width}x{height}, over {EDGE_LIMIT}x{EDGE_LIMIT}")
    if len(data) > BYTE_LIMIT:
        return fail(f"entry.png is {len(data)} bytes, over the {BYTE_LIMIT} byte limit")

    dest = out_dir / "entry.png"
    shutil.copyfile(PICTURE, dest)
    want = hashlib.sha256(data).hexdigest()
    got = hashlib.sha256(dest.read_bytes()).hexdigest()
    if got != want:
        return fail("written copy does not match the bundled picture")

    print(f"wrote {dest}: {len(data)} bytes, {width}x{height}, sha256={want}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
