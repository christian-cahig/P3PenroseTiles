"""
An adaptation of Example 3 in Christian Hill's tutorial at https://scipython.com/blog/penrose-tiling-2/

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

from core import PHI, PHI_SQUARED, LargeTile, Canvas

FILENAME_PREFIX = "example-03"

def load_arg_parser() -> Namespace:
    ap = ArgumentParser(
        description=(
            "Implements an adaptation of Example 3 in Christian Hill's tutorial "
            "at https://scipython.com/blog/penrose-tiling-2/"
        ),
        epilog=(
            "Tilings are saved as "
            f"'<SAVE_DIR>/{FILENAME_PREFIX}/<ROTATION>/<00,01,...,NUM_GENERATIONS>.svg'."
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
        "--rotation", type=float, default=0,
        help="Degrees (positive counterclockwise) by which the tiling is rotated"
    )
    ap.add_argument(
        "--save_dir", type=str, default="../outputs",
        help="Relative path to the directory where the tilings are saved",
    )

    return ap

if __name__ == "__main__":
    args = load_arg_parser().parse_args()

    theta = 0.4 * math.pi
    _a = complex(PHI*0.5*args.scale, 0)
    _v = complex(
        PHI*0.25*args.scale,
        math.sqrt((0.25 * (args.scale**2)) - (PHI_SQUARED * 0.0625 * (args.scale**2)))
    )
    As = [_a * complex(math.cos(i*theta), math.sin(i*theta)) for i in range(5)]
    Vs = [_v * complex(math.cos(i*theta), math.sin(i*theta)) for i in range(5)]
    starting_tiles = [LargeTile(a, v, complex(0, 0)) for (a, v) in zip(As, Vs)]

    for num_generations in range(args.num_generations+1):
        canvas = Canvas(
            scale=args.scale,
            num_generations=max(1, num_generations),
            starting_tiles=starting_tiles,
            config={"rotation" : math.radians(args.rotation)}
        )
        if num_generations: canvas.make_tiling()
        canvas.export_svg(
            filename=f"{num_generations:02d}",
            save_dir=f"{args.save_dir}/{FILENAME_PREFIX}/{args.rotation}",
        )
