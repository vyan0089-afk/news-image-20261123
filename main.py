#!/usr/bin/env python3
"""THE TWENTY-THIRD — make.fun news-image-20261123 entry.

Writes the entry image (Monday 23 November 2026 world news, one image)
to /output/entry.png. Standard library only; deterministic: the same
bytes are written on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
