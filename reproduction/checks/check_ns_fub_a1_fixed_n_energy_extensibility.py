#!/usr/bin/env python3
"""Exact N=1 implementation cross-check for fixed-N Galerkin extensibility.

The analytic all-fixed-N theorem is in paper/NS_FUB_A1_FIXED_N_EXTENSIBILITY_NO_GO.md.
This checker reconstructs the repository's exact integer-scaled N=1 quadratic tensor
C*B, forms the coordinate energy cubic polynomial, and verifies coefficient-by-
coefficient that the nonlinear contribution vanishes.  It also checks that the
scaled viscous diagonal is strictly negative on every retained nonzero mode.

This is a finite implementation calibration, not a machine proof of the all-N theorem.
"""
from __future__ import annotations

from collections import defaultdict
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_componentwise_radius as componentwise
import check_volume7_eps18_n1_explicit_radius as coarse


def physical_energy_weights(cube: base.CubeGalerkinModP) -> list[int]:
    # For one representative of each conjugate pair, e1/e2 are perpendicular basis
    # vectors with squared norms n1/n2.  The omitted common conjugate-pair factor 2
    # is irrelevant to exact cancellation and sign.
    weights: list[int] = []
    for _, _, n1, n2 in cube.bases:
        weights.extend([int(n1), int(n1), int(n2), int(n2)])
    return weights


def nonlinear_energy_polynomial(cube: base.CubeGalerkinModP):
    T = componentwise.scaled_bilinear_tensor(cube)
    weights = physical_energy_weights(cube)
    coeffs: dict[tuple[int, int, int], int] = defaultdict(int)
    nonzero_tensor_coeffs = 0

    # Q(x)=sum_i w_i x_i (C B(x,x))_i.
    # Aggregate into commutative cubic monomials x_a x_b x_c by sorting indices.
    for i in range(cube.d):
        wi = weights[i]
        for j in range(cube.d):
            row = T[i][j]
            for k in range(cube.d):
                value = int(row[k])
                if value:
                    nonzero_tensor_coeffs += 1
                    coeffs[tuple(sorted((i, j, k)))] += wi * value

    bad = {key: value for key, value in coeffs.items() if value != 0}
    return {
        "weights": weights,
        "tensor_nonzero_coefficients": nonzero_tensor_coeffs,
        "cubic_monomials_touched": len(coeffs),
        "bad_monomials": bad,
    }


def main() -> int:
    cube = base.CubeGalerkinModP()
    if cube.d != 52:
        raise AssertionError(f"expected N=1 dimension 52, got {cube.d}")

    energy = nonlinear_energy_polynomial(cube)
    if energy["bad_monomials"]:
        sample = list(energy["bad_monomials"].items())[:5]
        raise AssertionError(f"nonlinear energy polynomial did not cancel: {sample}")

    weights = energy["weights"]
    if min(weights) <= 0:
        raise AssertionError("energy coordinate weights must be positive")

    # C=600, nu=1/200, so C*(-nu |k|^2)=-3|k|^2 exactly.
    scaled_diag: list[int] = []
    k2_by_coordinate: list[int] = []
    for k in cube.reps:
        k2 = sum(int(v) * int(v) for v in k)
        scaled_diag.extend([-3 * k2] * 4)
        k2_by_coordinate.extend([k2] * 4)

    if len(scaled_diag) != cube.d or not all(d < 0 for d in scaled_diag):
        raise AssertionError("viscous scaled diagonal must be strictly negative")

    # Scaled derivative of the weighted quadratic energy has coefficients
    # 2*w_i*D_i on x_i^2; all must be strictly negative.
    linear_energy_coeffs = [2 * weights[i] * scaled_diag[i] for i in range(cube.d)]
    if not all(v < 0 for v in linear_energy_coeffs):
        raise AssertionError("linear energy coefficients must be strictly negative")

    normalization_ok = (
        coarse.C == 600
        and coarse.NU.numerator == 1
        and coarse.NU.denominator == 200
        and all(scaled_diag[i] == -coarse.C * coarse.NU.numerator * k2_by_coordinate[i] // coarse.NU.denominator for i in range(cube.d))
    )
    if not normalization_ok:
        raise AssertionError("C/nu viscous normalization mismatch")

    summary = {
        "cutoff": 1,
        "dimension": cube.d,
        "C": coarse.C,
        "nu": str(coarse.NU),
        "energy_weight_min": min(weights),
        "energy_weight_max": max(weights),
        "quadratic_tensor_nonzero_coefficients": energy["tensor_nonzero_coefficients"],
        "cubic_monomials_touched_before_cancellation": energy["cubic_monomials_touched"],
        "nonlinear_energy_bad_monomials": 0,
        "nonlinear_energy_polynomial_identically_zero": True,
        "scaled_viscous_diag_min": min(scaled_diag),
        "scaled_viscous_diag_max": max(scaled_diag),
        "linear_energy_coeff_max": max(linear_energy_coeffs),
        "strict_viscous_dissipation": True,
        "scope": "exact N=1 characteristic-zero implementation calibration; analytic fixed-N global extension is proved separately",
    }
    print("NS-FUB-A1 fixed-N energy/extensibility exact cross-check")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("NS-FUB-A1 FIXED-N ENERGY EXTENSIBILITY PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
