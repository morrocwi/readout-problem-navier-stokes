#!/usr/bin/env python3
"""Exact finite-field sanity check for the positive-viscosity scaling theorem.

The theorem itself is algebraic, not numerical:

    F_nu(nu y) = nu^2 F_1(y)

for F_nu(x) = nu A x + B(x,x), with B quadratic. Since every shell-energy
component and total energy are quadratic, their Lie jets differ across positive
viscosities only by nonzero row and state scalings.

This script reuses the exact K=1 Galerkin operator from
check_volume6_ns_observability.py and checks the vector-field and quadratic-reader
scaling identities modulo the same good prime. It is a reproducibility sanity
check, not the proof of the theorem.
"""
from __future__ import annotations

from fractions import Fraction
import json
import sys

import numpy as np

from check_volume6_ns_observability import CubeGalerkinModP, P


def frac_mod(q: Fraction) -> int:
    return q.numerator * pow(q.denominator, -1, P) % P


def field(cube: CubeGalerkinModP, x: np.ndarray, nu_mod: int) -> np.ndarray:
    k2_diag = np.repeat(cube.k2_rep, 4).astype(np.int64)
    linear = (-nu_mod * k2_diag % P) * (x % P) % P
    return (linear + cube.bilinear(x, x)) % P


def shell_energy(cube: CubeGalerkinModP, x: np.ndarray) -> np.ndarray:
    x2 = (x % P) * (x % P) % P
    return x2 @ cube.weights.T % P


def run_check(seed: int = 20260910) -> tuple[bool, dict]:
    cube = CubeGalerkinModP()
    rng = np.random.default_rng(seed)
    y = rng.integers(1, P, size=cube.d, dtype=np.int64)

    viscosities = [
        Fraction(1, 200),
        Fraction(1, 1),
        Fraction(7, 19),
        Fraction(37, 113),
    ]

    base_field = field(cube, y, 1)
    base_shell = shell_energy(cube, y)
    checks = []

    for nu in viscosities:
        n = frac_mod(nu)
        x = n * y % P
        vector_ok = np.array_equal(
            field(cube, x, n),
            n * n % P * base_field % P,
        )
        reader_ok = np.array_equal(
            shell_energy(cube, x),
            n * n % P * base_shell % P,
        )
        checks.append(
            {
                "nu": str(nu),
                "nu_mod_p": int(n),
                "vector_field_scaling": bool(vector_ok),
                "shell_energy_scaling": bool(reader_ok),
            }
        )

    # Inviscid endpoint sanity check: the quadratic Galerkin interaction conserves
    # total retained kinetic energy. This is deliberately separate from nu > 0.
    total_weight = np.sum(cube.weights, axis=0) % P
    f0 = field(cube, y, 0)
    dE0 = int((2 * np.sum((total_weight * y % P) * f0 % P)) % P)
    inviscid_energy_conservation = dE0 == 0

    ok = all(
        item["vector_field_scaling"] and item["shell_energy_scaling"]
        for item in checks
    ) and inviscid_energy_conservation

    report = {
        "prime": P,
        "state_dimension": cube.d,
        "checks": checks,
        "inviscid_total_energy_derivative_mod_p": dE0,
        "inviscid_energy_conservation": inviscid_energy_conservation,
        "status": "PASS" if ok else "FAIL",
    }
    return ok, report


def main() -> int:
    ok, report = run_check()
    print("[positive-viscosity scaling identity]")
    for item in report["checks"]:
        print(
            "  nu=", item["nu"],
            " vector=", item["vector_field_scaling"],
            " shell_energy=", item["shell_energy_scaling"],
            sep="",
        )
    print("  inviscid dE/dt mod p =", report["inviscid_total_energy_derivative_mod_p"])
    print("RESULT_JSON:" + json.dumps(report, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
