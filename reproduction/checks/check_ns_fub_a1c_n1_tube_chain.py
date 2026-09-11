#!/usr/bin/env python3
"""Exact finite multi-step tube-chain verifier/generator for NS-FUB-A1C.

This extends the single-step N=1 validated tube calibration into a finite chain.
Each step starts from a rational interval box I_m known to contain the actual
finite Galerkin state.  A larger rational tube X_m is chosen around the same
coordinate center and exact bounds certify

    I_m subset X_m,
    I_m + [0,h_m] F(X_m) subset X_m,
    h_m L_m <= 1/2.

For every initial point in I_m the Picard operator is therefore a contraction in
X_m.  The endpoint is enclosed by I_m + [-h_m M_i, h_m M_i], which becomes the
next initial interval I_{m+1}.  Finite induction composes the certified steps.

This script automatically constructs four such fixed-N=1 steps with exact
rational arithmetic and feeds the final box to the A1V H^3 verifier.

It is NOT a proof that the chain reaches an arbitrary requested time, NOT an
arbitrary-N generator, and NOT a global-regularity argument.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(100_000)

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_componentwise_radius as component
import check_volume7_eps18_n1_explicit_radius as coarse
import check_volume7_eps18_n1_small_witness as small
import check_ns_fub_a1_h3_certificate as h3
import check_ns_fub_a1c_n1_validated_tube as one_step

C = coarse.C
CENTER_SEED = 20260910
BASE_SLACK = Fraction(1, 1000)
STEPS = 4
H3_THRESHOLD = Fraction(1)


def frac_text(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def vector_field_bounds_from_sparse(cube, sparse_T, x0, tube_radius: Fraction):
    d = cube.d
    R = [Fraction(abs(int(x0[j]))) + tube_radius for j in range(d)]
    scaled_linear = [
        -3 * sum(int(v) * int(v) for v in k)
        for k in cube.reps
        for _ in range(4)
    ]
    M = []
    L_rows = []
    for i, entries in enumerate(sparse_T):
        f_abs = Fraction(abs(scaled_linear[i])) * R[i]
        lip = Fraction(abs(scaled_linear[i]))
        for j, k, coeff_int in entries:
            coeff = Fraction(coeff_int)
            f_abs += coeff * R[j] * R[k]
            lip += coeff * (R[j] + R[k])
        M.append(f_abs / C)
        L_rows.append(lip / C)
    return M, max(L_rows)


def choose_certified_step(widths, tube_radius: Fraction, M, L: Fraction) -> Fraction:
    if L <= 0:
        raise ArithmeticError("nonpositive Lipschitz bound")
    candidates = [Fraction(1, 2) / L]
    for w, m in zip(widths, M):
        slack = tube_radius - w
        if slack <= 0:
            raise ArithmeticError("initial interval is not strictly inside proposed tube")
        if m > 0:
            # Half of the available displacement slack, leaving an explicit margin.
            candidates.append(slack / (2 * m))
    h = min(candidates)
    if h <= 0:
        raise ArithmeticError("failed to construct positive step")
    return h


def main() -> int:
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"]:
        raise RuntimeError("declared deterministic N=1 center did not reproduce")
    x0 = small.small_state(CENTER_SEED, cube.d)

    T = component.scaled_bilinear_tensor(cube)
    sparse_T = component.sparse_absolute_tensor(T)
    tensor_nonzero = sum(len(row) for row in sparse_T)
    tensor_inf = max(sum(coeff for _, _, coeff in row) for row in sparse_T)
    if tensor_nonzero != 2096 or tensor_inf != 36000:
        raise AssertionError("exact tensor audit drift")

    widths = [Fraction(0) for _ in range(cube.d)]
    total_time = Fraction(0)
    records = []

    for step in range(STEPS):
        wmax = max(widths)
        # Keep a positive fresh margin beyond the incoming interval width.
        tube_radius = 2 * wmax + BASE_SLACK
        M, L = vector_field_bounds_from_sparse(cube, sparse_T, x0, tube_radius)
        h = choose_certified_step(widths, tube_radius, M, L)

        self_ratios = [
            (widths[i] + h * M[i]) / tube_radius
            for i in range(cube.d)
        ]
        self_ratio = max(self_ratios)
        contraction = h * L
        if self_ratio >= 1 or contraction >= 1:
            raise AssertionError("step failed strict self-map/contraction gate")

        new_widths = [widths[i] + h * M[i] for i in range(cube.d)]
        if any(new_widths[i] > tube_radius for i in range(cube.d)):
            raise AssertionError("endpoint enclosure escaped certified tube")

        total_time += h
        records.append(
            {
                "step": step + 1,
                "tube_radius": frac_text(tube_radius),
                "incoming_max_halfwidth": frac_text(wmax),
                "h": frac_text(h),
                "L": frac_text(L),
                "contraction_q": frac_text(contraction),
                "self_map_ratio": frac_text(self_ratio),
                "outgoing_max_halfwidth": frac_text(max(new_widths)),
                "cumulative_time": frac_text(total_time),
            }
        )
        widths = new_widths

    final_box = [
        (Fraction(int(x0[i])) - widths[i], Fraction(int(x0[i])) + widths[i])
        for i in range(cube.d)
    ]
    mode_records = one_step.full_fourier_mode_records(cube, final_box)
    h3_status, h3_margin = h3.verdict(mode_records, H3_THRESHOLD)
    h3_lower = h3.h3_squared_lower(mode_records)
    if h3_status != "PASS":
        raise AssertionError("final chained enclosure lost fixed H3 calibration witness")

    # The chain must make strict forward progress beyond the one-step duration.
    first_h = Fraction(records[0]["h"])
    if total_time <= first_h:
        raise AssertionError("multi-step chain did not advance beyond first step")

    summary = {
        "cutoff": 1,
        "dimension": cube.d,
        "steps": STEPS,
        "center_seed": CENTER_SEED,
        "base_slack": frac_text(BASE_SLACK),
        "exact_tensor_nonzero_coefficients": tensor_nonzero,
        "exact_tensor_infinity_row_sum": tensor_inf,
        "total_certified_time": frac_text(total_time),
        "final_max_halfwidth": frac_text(max(widths)),
        "final_H3_threshold": frac_text(H3_THRESHOLD),
        "final_H3_squared_lower": frac_text(h3_lower),
        "final_H3_margin": frac_text(h3_margin),
        "final_H3_certificate": h3_status,
        "chain": records,
        "scope": (
            "fixed N=1, four-step exact rational certificate chain; no arbitrary target-time "
            "termination, no arbitrary-N generator, no Clay conclusion"
        ),
    }
    print("NS-FUB-A1C N=1 finite validated tube chain")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("NS-FUB-A1C N1 TUBE CHAIN PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
