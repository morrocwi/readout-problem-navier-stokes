#!/usr/bin/env python3
"""Compatibility runner for the practical Arb validator.

The reusable componentwise checker returns its exact tensor as nested Python lists.
The validator also needs NumPy sparse indexing, so normalize that return value to an
object ndarray without changing any coefficient.  The first h=1/14 validation attempt
failed its step-0 bootstrap on an 8-substep-per-sample mesh; use 32 substeps here so the
a-posteriori residual gate is tested on a four-times finer declared mesh.
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

validator.SUBSTEPS_PER_SAMPLE = 32

if __name__ == "__main__":
    raise SystemExit(validator.main())
