#!/usr/bin/env python3
"""Exact regression controls for NS-FUB-A1 energy-only H3 tail no-go.

The analytic theorem is in paper/NS_FUB_A1_H3_TAIL_NO_GO.md. This script does not
machine-prove the quantified theorem; it verifies representative instances using
Fraction-only arithmetic and checks the finite-band / stronger-weight repair formulas.
"""
from fractions import Fraction
import json


def witness(N: int, eps: Fraction, B: Fraction):
    if N < 0 or eps <= 0 or B <= 0:
        raise ValueError("need N>=0, eps>0, B>0")
    a = eps / 2
    K = N + 1
    while True:
        l2_sq = 2 * a * a
        h3_sq = 2 * Fraction((1 + K * K) ** 3) * a * a
        if h3_sq > B * B:
            break
        K += 1
    return {
        "N": N,
        "eps": str(eps),
        "B": str(B),
        "K": K,
        "amplitude": str(a),
        "divergence_dot": 0,  # (K,0,0) dot (0,1,0)
        "l2_sq": str(l2_sq),
        "eps_sq": str(eps * eps),
        "h3_sq": str(h3_sq),
        "B_sq": str(B * B),
        "support_above_cutoff": K > N,
        "l2_ok": l2_sq <= eps * eps,
        "h3_exceeds": h3_sq > B * B,
    }


def finite_band_guard(N: int, M: int, energy_sq: Fraction):
    if not (0 <= N < M) or energy_sq < 0:
        raise ValueError("bad band")
    return Fraction((1 + M * M) ** 3) * energy_sq


def stronger_weight_guard(N: int, sigma: int, h3sigma_tail_sq: Fraction):
    if N < 0 or sigma <= 0 or h3sigma_tail_sq < 0:
        raise ValueError("bad weighted tail")
    return h3sigma_tail_sq / Fraction((1 + N * N) ** sigma)


def main() -> int:
    cases = [
        (1, Fraction(1, 10), Fraction(10)),
        (8, Fraction(1, 1000), Fraction(10**6)),
        (32, Fraction(1, 10**9), Fraction(10**12)),
        (100, Fraction(3, 10**7), Fraction(10**15)),
    ]
    records = [witness(*c) for c in cases]
    if not all(r["support_above_cutoff"] and r["l2_ok"] and r["h3_exceeds"] and r["divergence_dot"] == 0 for r in records):
        raise AssertionError("single-mode tail witness failed")

    # Finite-band estimate is valid but the coefficient grows rapidly with M.
    e2 = Fraction(1, 10**12)
    fb_10 = finite_band_guard(8, 10, e2)
    fb_100 = finite_band_guard(8, 100, e2)
    if not fb_100 > fb_10:
        raise AssertionError("finite-band H3 multiplier should grow with outer cutoff")

    # Stronger weighted budget yields a decaying H3 tail envelope.
    C = Fraction(7, 3)
    repaired_8 = stronger_weight_guard(8, 1, C)
    repaired_80 = stronger_weight_guard(80, 1, C)
    if not repaired_80 < repaired_8:
        raise AssertionError("H^{3+sigma} repair envelope should decay with cutoff")

    summary = {
        "witnesses": records,
        "finite_band_example": {
            "N": 8,
            "energy_sq": str(e2),
            "M10_H3_sq_upper": str(fb_10),
            "M100_H3_sq_upper": str(fb_100),
            "outer_cutoff_growth_confirmed": fb_100 > fb_10,
        },
        "stronger_weight_repair_example": {
            "sigma": 1,
            "C": str(C),
            "N8_H3_tail_sq_upper": str(repaired_8),
            "N80_H3_tail_sq_upper": str(repaired_80),
            "decay_confirmed": repaired_80 < repaired_8,
        },
        "scope": "exact finite regression controls; the quantified Fourier no-go theorem is analytic, not machine-proved by this script",
    }
    print("NS-FUB-A1 energy-only H3 tail no-go controls")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("NS-FUB-A1 H3 TAIL NO-GO CONTROLS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
