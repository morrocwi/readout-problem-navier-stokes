#!/usr/bin/env python3
"""Compatibility runner for the practical Arb validator.

The reusable componentwise checker returns its exact tensor as nested Python lists.
The validator also needs NumPy sparse indexing, so normalize that return value to an
object ndarray without changing any coefficient.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume7_eps18_n1_componentwise_radius as comp

_original = comp.scaled_bilinear_tensor
comp.scaled_bilinear_tensor = lambda cube: np.asarray(_original(cube), dtype=object)

import check_volume7_eps19_n1_practical_arb_validator as validator

if __name__ == "__main__":
    raise SystemExit(validator.main())
