#!/usr/bin/env python3
"""Compatibility/tight-bootstrap runner for the practical Arb validator.

The exact coefficient tensor is normalized from nested lists to an object ndarray.
The original validator's bootstrap searched for a self-consistent error cap by doubling;
for a quadratic inequality that can jump across the admissible interval.  Here we use a
monotone fixed-point inflation and accept a cap only after the exact Arb inequality
``rhs <= cap`` is verified.  This changes search sharpness, not the proof obligation.
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


def tight_state_sup(e0, dt, R, K0, D2):
    one = validator.arb(1)
    denom0 = one - dt * K0
    if not (validator.arb(0) < denom0):
        return None
    cap = validator.up((e0 + dt * R) / denom0)
    inflate = validator.arb("1.000001")
    tiny = validator.arb("1e-45")
    for _ in range(300):
        K = validator.up(K0 + D2 * cap)
        if not (dt * K < 1):
            return None
        rhs = validator.up(e0 + dt * (R + K * cap))
        if rhs <= cap:
            return cap, rhs, K
        cap = validator.up(rhs * inflate + tiny)
    return None


def tight_branch_state_sup(p0, dt, Kc, Binf):
    cap = validator.up(p0)
    inflate = validator.arb("1.000001")
    tiny = validator.arb("1e-50")
    for _ in range(300):
        rhs = validator.up(p0 + dt * (Kc * cap + Binf * cap * cap))
        if rhs <= cap:
            return cap, rhs
        cap = validator.up(rhs * inflate + tiny)
    return None


validator.choose_state_sup = tight_state_sup
validator.choose_branch_state_sup = tight_branch_state_sup

if __name__ == "__main__":
    raise SystemExit(validator.main())
