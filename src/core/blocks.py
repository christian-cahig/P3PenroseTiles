"""
Building blocks

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

from math import isclose

from .utils import PHI, PSI, PSI_SQUARED

__all__ = ["RobinsonTriangle", "LargeTile", "SmallTile"]

Point : TypeAlias = complex
SVGPathDefn : TypeAlias = str
ArcPathDefns = tuple[SVGPathDefn, SVGPathDefn]

class RobinsonTriangle:
    """
    Robinson triangle and the rhombus formed by its mirror image about its base

    This implementation is based on Christian Hill's tutorial at
        https://scipython.com/blog/penrose-tiling-1/,
        https://scipython.com/blog/penrose-tiling-2/, and
        https://github.com/xnx/penrose.

    Parameters
    -------
    A, V, B
        Complex numbers indicating the (ordered) vertices
        `V` is at the vertex angle. `A` and `B` define the base.
        `A`-to-`V` and `B`-to-`V` distances must be equal (up to numerical precision).
    """
    def __init__(
        self,
        A : Point,
        V : Point,
        B : Point,
    ) -> Self:
        self.A = A if isinstance(A, Point) else Point(A)
        self.vertex = V if isinstance(V, Point) else Point(V)
        self.B = B if isinstance(B, Point) else Point(B)

        assert isclose(abs(self.A - self.vertex), abs(self.B - self.vertex))

    def leg_length(self) -> float: return abs(self.A - self.vertex)

    def base_length(self) -> float: return abs(self.A - self.B)

    def base_midpoint(self) -> Point: return (self.A + self.B) / 2

    def center(self) -> Point: return (self.base_midpoint + self.vertex) / 2

    def rhombus_center(self) -> Point: return self.base_midpoint()

    def path(self) -> SVGPathDefn:
        AV, VB = self.vertex - self.A, self.B - self.vertex
        return (
            f"m{self.A.real},{self.A.imag} "
            f"l{AV.real},{AV.imag} "
            f"l{VB.real},{VB.imag}z"
        )

    def rhombus_path(self) -> SVGPathDefn:
        AV, VB = self.vertex - self.A, self.B - self.vertex
        return (
            f"m{self.A.real},{self.A.imag} "
            f"l{AV.real},{AV.imag} "
            f"l{VB.real},{VB.imag} "
            f"l{-AV.real},{-AV.imag}z"
        )

    @staticmethod
    def arc_path_defn(
        V : Point,
        F : Point,
        T : Point,
        use_rhombus : bool = False,
    ) -> SVGPathDefn:
        V = V if isinstance(V, Point) else Point(V)
        F = F if isinstance(F, Point) else Point(F)
        T = T if isinstance(T, Point) else Point(T)
        assert abs(F - V) == abs(T - V)
        start_point = (V + F) / 2
        end_point = (V + T) / 2
        arc_radius = abs((F - V) / 2)

        if not use_rhombus:
            VN = F + T - (2*V)
            end_point = V + (arc_radius * (VN / abs(VN)))

        # Ensure that the arc subtends an angle less than 180°
        VS, VE = start_point - V, end_point - V
        if ((VS.real * VE.imag) - (VS.imag * VE.real)):
            start_point, end_point = end_point, start_point

        return (
            f"M {start_point.real} {start_point.imag} "
            f"A {arc_radius} {arc_radius} "
            f"0 0 0 {end_point.real} {end_point.imag}"
        )

    def get_arc_paths(
        self,
        use_rhombus : bool = False,
    ) -> ArcPathDefns:
        D = self.A - self.vertex + self.B
        return (
            self.arc_path_defn(self.A, self.vertex, D, use_rhombus=use_rhombus),
            self.arc_path_defn(self.B, self.vertex, D, use_rhombus=use_rhombus),
        )

    def arc_paths(self) -> ArcPathDefns: return self.get_arc_paths(use_rhombus=False)

    def rhombus_arc_paths(self) -> ArcPathDefns: return self.get_arc_paths(use_rhombus=True)

    def conjugate(self) -> RobinsonTriangle:
        return self.__class__(self.A.conjugate(), self.vertex.conjugate(), self.B.conjugate())

class LargeTile(RobinsonTriangle):
    """
    Tile based on Robinson triangle with sides in ratio 1:1:phi

    This implementation is based on Christian Hill's tutorial at
        https://scipython.com/blog/penrose-tiling-1/,
        https://scipython.com/blog/penrose-tiling-2/, and
        https://github.com/xnx/penrose.

    Parameters
    -------
    A, V, B
        Complex numbers indicating the (ordered) vertices
        `V` is at the vertex angle. `A` and `B` define the base.
        `A`-to-`V` and `B`-to-`V` distances must be equal (up to numerical precision).
    """
    def __init__(
        self,
        A : Point,
        V : Point,
        B : Point,
    ) -> Self:
        super().__init__(A, V, B)
        assert isclose(self.base_length() / self.leg_length(), PHI)

    def inflate(self) -> list[LargeTile, SmallTile, LargeTile]:
        D = (PSI_SQUARED * self.A) + (PSI * self.B)
        E = (PSI_SQUARED * self.A) + (PSI * self.vertex)
        return [
            LargeTile(D, E, self.A),
            SmallTile(E, D, self.vertex),
            LargeTile(self.B, D, self.vertex),
        ]

class SmallTile(RobinsonTriangle):
    """
    Tile based on Robinson triangle with sides in ratio 1:1:psi

    This implementation is based on Christian Hill's tutorial at
        https://scipython.com/blog/penrose-tiling-1/,
        https://scipython.com/blog/penrose-tiling-2/, and
        https://github.com/xnx/penrose.

    Parameters
    -------
    A, V, B
        Complex numbers indicating the (ordered) vertices
        `V` is at the vertex angle. `A` and `B` define the base.
        `A`-to-`V` and `B`-to-`V` distances must be equal (up to numerical precision).
    """
    def __init__(
        self,
        A : Point,
        V : Point,
        B : Point,
    ) -> Self:
        super().__init__(A, V, B)
        assert isclose(self.base_length() / self.leg_length(), PSI)

    def inflate(self) -> list[SmallTile, LargeTile]:
        D = (PSI * self.A) + (PSI_SQUARED * self.vertex)
        return [
            SmallTile(D, self.B, self.A),
            LargeTile(self.B, D, self.vertex),
        ]
