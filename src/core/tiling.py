"""
Tiling functionalities

P3PenroseTiles
Copyright (C) 2023 - present, Christian Cahig
https://github.com/christian-cahig/P3PenroseTiles

This file is part of the repository P3PenroseTiles, and is covered by the CC-BY-4.0 License.
See `LICENSE` in the root of the repository for details.
"""
from __future__ import annotations

from numbers import Complex
from typing import TypeAlias
from typing_extensions import Self
from os import PathLike
from pathlib import Path

from math import isclose, sqrt, sin, cos

from .blocks import Point, SVGPathDefn, LargeTile, SmallTile
from .utils import PSI

__all__ = ["Canvas", "get_default_config"]

Config : TypeAlias = dict[str, str | float | bool]
CanvasElements : TypeAlias = list[LargeTile | SmallTile, ...]

def get_default_config() -> Config: return {
    "margin" : 0.0,
    # 
    "stroke-color" : "#FFFFFF",
    # 
    "reflect-x" : True,
    "rotation" : 0,
    # 
    "large-tile-color" : "#B31B1B",
    "small-tile-color" : "#B31B1B",
    "large-tile-opacity" : 0.90,
    "small-tile-opacity" : 0.37,
    # 
    "equality-tol" : 0,
}

class Canvas:
    """
    Canvas containing the P3 Penrose tiling
    Robinson triangle and the rhombus formed by its mirror image about its base

    This implementation is based on Christian Hill's tutorial at
        https://scipython.com/blog/penrose-tiling-1/,
        https://scipython.com/blog/penrose-tiling-2/, and
        https://github.com/xnx/penrose.

    Parameters
    -------
    scale : int
    A, V, B
        Complex numbers indicating the (ordered) vertices
        `V` is at the vertex angle. `A` and `B` define the base.
        `A`-to-`V` and `B`-to-`V` distances must be equal (up to numerical precision).
    """
    def __init__(
        self,
        scale : float = 200,
        num_generations : int = 5,
        config : Config = {},
        starting_tiles : CanvasElements | None = None,
    ) -> Self:
        assert (scale > 0) and (num_generations > 0)
        self.scale = scale
        self.num_generations = num_generations

        self.config = get_default_config()
        self.config.update(config)
        assert 0 <= self.config['margin'] < 1.0
        assert not isinstance(self.config['rotation'], complex)
        assert self.config['equality-tol'] >= 0.0

        self.reset_elements(starting_tiles=starting_tiles)

    def reset_elements(
        self,
        starting_tiles : CanvasElements | None = None,
    ) -> Self:
        assert all(
            (isinstance(e, LargeTile) or isinstance(e, SmallTile)) \
                for e in starting_tiles
        ) if starting_tiles else True
        self.elements = starting_tiles

    def inflate(self) -> Self:
        assert len(self.elements) > 0, "Canvas is not yet initialized."
        new_elements = []
        for e in self.elements: new_elements.extend(e.inflate())
        self.elements = new_elements

    def remove_duplicates(self) -> Self:
        assert len(self.elements) > 0, "Canvas is not yet initialized."
        sorted_elements = sorted(
            self.elements,
            key=lambda e : (e.rhombus_center().real, e.rhombus_center().imag)
        )
        self.elements = [sorted_elements[0]]
        for i, e in enumerate(sorted_elements[1:], start=1):
            if not isclose(
                abs(e.rhombus_center() - sorted_elements[i-1].rhombus_center()), 0,
                abs_tol=self.config['equality-tol']
            ): self.elements.append(e)

    def add_conjugate_elements(self) -> Self:
        assert len(self.elements) > 0, "Canvas is not yet initialized."
        self.elements.extend([e.conjugate() for e in self.elements])

    def rotate(self) -> Self:
        assert len(self.elements) > 0, "Canvas is not yet initialized."
        rotator = complex(cos(self.config['rotation']), sin(self.config['rotation']))
        for e in self.elements:
            e.A *= rotator
            e.vertex *= rotator
            e.B *= rotator

    def flip_about_yaxis(self) -> Self:
        assert len(self.elements) > 0, "Canvas is not yet initialized."
        for e in self.elements:
            e.A = complex(-e.A.real, e.A.imag)
            e.vertex = complex(-e.vertex, e.B.imag)
            e.B = complex(-e.B.real, e.B.imag)

    def flip_about_xaxis(self) -> Self:
        assert len(self.elements) > 0, "Canvas is not yet initialized."
        for e in self.elements:
            e.A = e.A.conjugate()
            e.vertex = e.vertex.conjugate()
            e.B = e.B.conjugate()

    def make_tiling(self) -> Self:
        for _ in range(self.num_generations): self.inflate()
        self.remove_duplicates()
        if self.config['reflect-x']: self.add_conjugate_elements(); self.remove_duplicates()
        if self.config['rotation']: self.rotate()

    def get_tile_color(
        self,
        tile : LargeTile | SmallTile,
    ) -> str:
        return self.config['large-tile-color'] if isinstance(tile, LargeTile) \
            else self.config['small-tile-color']

    def get_SVG_code(self) -> str:
        assert len(self.elements) > 0, "Canvas is not yet initialized."
        x_min = y_min = -self.scale * (1 + self.config['margin'])
        width = height = 2 * self.scale * (1 + self.config['margin'])
        viewBox = f"{x_min} {y_min} {width} {height}"

        svg = [
            '<?xml version="1.0" encoding="utf-8"?>',
            (
                '<svg width="100%" height="100%" viewBox="{}"'
                ' preserveAspectRatio="xMidYMid meet" version="1.1"'
                ' baseProfile="full" xmlns="http://www.w3.org/2000/svg">'
            ).format(viewBox)
        ]
        svg.append('<g style="stroke:{}; stroke-width: {}; stroke-linejoin: round;">'.format(
            self.config['stroke-color'], str(0.03 * (PSI**self.num_generations) * self.scale)
        ))
        for e in self.elements:
            svg.append('<path fill="{}" fill-opacity="{}" d="{}"/>'.format(
                self.get_tile_color(e),
                self.config['large-tile-opacity'] if isinstance(e, LargeTile) \
                    else self.config['small-tile-opacity'],
                e.rhombus_path()
            ))
        svg.append('</g>\n</svg>')

        return "\n".join(svg)

    def export_svg(
        self,
        filename : str = "tiling",
        save_dir : PathLike = "./",
    ) -> None:
        save_dir = Path(save_dir); save_dir.mkdir(parents=True, exist_ok=True)
        save_dir.joinpath(f"{filename}.svg").write_text(self.get_SVG_code())
