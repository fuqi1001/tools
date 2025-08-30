#!/usr/bin/env python3
# python make_blob_file.py
# python make_blob_file.py 200 /tmp/test_200mb.bin
# python make_blob_file.py 200 /tmp/test_200mb_random.bin random
# python make_blob_file.py 200 /tmp/test_200mb_pat.bin pattern

import os, sys

SIZE_MB   = int(sys.argv[1]) if len(sys.argv) > 1 else 200
OUT_PATH  = sys.argv[2] if len(sys.argv) > 2 else f"sample_{SIZE_MB}MB.bin"
MODE      = sys.argv[3] if len(sys.argv) > 3 else "zero"  # zero | random | pattern

CHUNK = 4 * 1024 * 1024  # 4 MiB
remaining = SIZE_MB * 1024 * 1024

if MODE == "pattern":
    block = (b"MEDUSA_TEST_" * ((CHUNK // len(b"MEDUSA_TEST_")) + 1))[:CHUNK]
elif MODE == "zero":
    block = bytes(CHUNK)
elif MODE == "random":
    block = None
else:
    raise SystemExit("MODE must be zero | random | pattern")

with open(OUT_PATH, "wb") as f:
    while remaining > 0:
        to_write = min(CHUNK, remaining)
        data = os.urandom(to_write) if MODE == "random" else block[:to_write]
        f.write(data)
        remaining -= to_write

print(f"Wrote {SIZE_MB} MiB -> {OUT_PATH}")
