"""
An adaptation of Example 2 in Christian Hill's tutorial at https://scipython.com/blog/penrose-tiling-2/

P3PenroseTiles
Copyright (C) 2023 - present, Christian Cahig
https://github.com/christian-cahig/P3PenroseTiles

This file is part of the repository P3PenroseTiles, and is covered by the CC-BY-4.0 License.
See `LICENSE` in the root of the repository for details.
"""
from __future__ import annotations
from argparse import ArgumentParser, Namespace
from pathlib import Path
import pickle as pkl

import math

from core import SmallTile, Canvas

FILENAME_PREFIX = "example-02"

def load_arg_parser() -> Namespace:
    ap = ArgumentParser(
        description=(
            "Implements an adaptation of Example 2 in Christian Hill's tutorial "
            "at https://scipython.com/blog/penrose-tiling-2/"
        ),
        epilog=(
            "Tilings are saved as "
            f"'<SAVE_DIR>/{FILENAME_PREFIX}/<00,01,...,NUM_GENERATIONS>.svg'."
        ),
    )
    ap.add_argument(
        "--num_generations", type=int, default=5,
        help="Number of generations, i.e., times inflation is applied",
    )
    ap.add_argument(
        "--scale", type=float, default=70,
        help="Scale factor determining the size of the image",
    )
    ap.add_argument(
        "--save_dir", type=str, default="../outputs",
        help="Relative path to the directory where the tilings are saved",
    )

    return ap

if __name__ == "__main__":
    args = load_arg_parser().parse_args()

    theta = math.pi / 5
    rotator = complex(math.cos(theta), math.sin(theta))
    V = complex(0, 0)
    A1 = complex(0.5 * args.scale, 0)
    B1 = B2 = (A1 * rotator)
    A2 = A3 = (B1 * rotator)
    B3 = B4 = (A3 * rotator)
    A4 = A5 = (B4 * rotator)
    B5 = -A1
    starting_tiles = [
        SmallTile(A1, V, B1),
        SmallTile(A2, V, B2),
        SmallTile(A3, V, B3),
        SmallTile(A4, V, B4),
        SmallTile(A5, V, B5),
    ]

    for num_generations in range(args.num_generations+1):
        canvas = Canvas(
            scale=args.scale,
            num_generations=max(1, num_generations),
            starting_tiles=starting_tiles,
        )
        if num_generations: canvas.make_tiling()
        canvas.export_svg(
            filename=f"{num_generations:02d}",
            save_dir=f"{args.save_dir}/{FILENAME_PREFIX}",
        )
