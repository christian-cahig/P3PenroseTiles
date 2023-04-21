"""
Miscellaneous utilities

P3PenroseTiles
Copyright (C) 2023 - present, Christian Cahig
https://github.com/christian-cahig/P3PenroseTiles

This file is part of the repository P3PenroseTiles, and is covered by the CC-BY-4.0 License.
See `LICENSE` in the root of the repository for details.
"""
from __future__ import annotations

from math import sqrt

__all__ = ["PHI", "PSI", "PHI_SQUARED", "PSI_SQUARED"]

PHI = (sqrt(5) + 1) / 2
PSI = (sqrt(5) - 1) / 2
PHI_SQUARED = 1.5 + (0.5*sqrt(5))
PSI_SQUARED = 1 - PSI
