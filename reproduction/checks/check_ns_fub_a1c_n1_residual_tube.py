#!/usr/bin/env python3
"""Exact residual-centered validated tube for NS-FUB-A1C-G localization.

The earlier absolute tube is sound but coarse: it encloses the endpoint around the
old center using |F|.  This checker validates an affine rational reference path

    p(t) = a + t v,   v = F(a),

and an error tube ||x(t)-p(t)||_inf <= r.  On the full path/error tube it computes
exact rational interval bounds

    R >= ||F(p(t)+e) - v||_inf,
    L >= ||DF||_inf.

For exact initial point a, the fail-closed gates

    h R <= r,
    h L < 1

make the Picard error operator a self-map and contraction.  The endpoint is then
localized around the moved center p(h), not the old state.

The script also contains the exact negative control x'=1: absolute propagation
has final halfwidth T independent of mesh refinement, whereas p(t)=t has residual
zero and exact endpoint localization.

Scope: fixed N=1 calibration only.  No arbitrary-target termination, arbitrary-N
constructor, singularity capture, or Clay conclusion.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Tuple

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
import check_ns_fub_a1c_n1_validated_tube as absolute

C = coarse.C
CENTER_SEED = 20260910
H3_THRESHOLD = Fraction(1)

Interval = Tuple[Fraction, Fraction]


def add_iv(a: Interval, b: Interval) -> Interval:
    return a[0] + b[0], a[1] + b[1]


def sub_iv(a: Interval, b: Interval) -> Interval:
    return a[0] - b[1], a[1] - b[0]


def scale_iv(c: int | Fraction, a: Interval) -> Interval:
    c = Fraction(c)
    if c >= 0:
        return c * a[0], c * a[1]
    return c * a[1], c * a[0]


def mul_iv(a: Interval, b: Interval) -> Interval:
    vals = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return min(vals), max(vals)


def maxabs_iv(a: Interval) -> Fraction:
    return max(abs(a[0]), abs(a[1]))


def scaled_linear_diag(cube) -> list[int]:
    return [
        -3 * sum(int(v) * int(v) for v in k)
        for k in cube.reps
        for _ in range(4)
    ]


def eval_F_point(cube, sparse_signed_T, x) -> list[Fraction]:
    D = scaled_linear_diag(cube)
    out = []
    for i, entries in enumerate(sparse_signed_T):
        acc = Fraction(D[i] * int(x[i]))
        for j, k, coeff in entries:
            acc += Fraction(coeff) * Fraction(int(x[j])) * Fraction(int(x[k]))
        out.append(acc / C)
    return out


def signed_sparse_tensor(T):
    out = []
    for row in T:
        entries = []
        for j, col in enumerate(row):
            for k, coeff in enumerate(col):
                coeff = int(coeff)
                if coeff:
                    entries.append((j, k, coeff))
        out.append(entries)
    return out


def affine_path_tube(a, v, h: Fraction, r: Fraction) -> list[Interval]:
    X = []
    for ai, vi in zip(a, v):
        ai = Fraction(int(ai))
        end = ai + h * vi
        lo_p, hi_p = min(ai, end), max(ai, end)
        X.append((lo_p - r, hi_p + r))
    return X


def interval_F_and_L(cube, signed_T, X: list[Interval]):
    D = scaled_linear_diag(cube)
    Fivs = []
    Lrows = []
    Rabs = [maxabs_iv(iv) for iv in X]
    for i, entries in enumerate(signed_T):
        acc = scale_iv(D[i], X[i])
        lip = Fraction(abs(D[i]))
        for j, k, coeff in entries:
            acc = add_iv(acc, scale_iv(coeff, mul_iv(X[j], X[k])))
            lip += Fraction(abs(coeff)) * (Rabs[j] + Rabs[k])
        Fivs.append(scale_iv(Fraction(1, C), acc))
        Lrows.append(lip / C)
    return Fivs, max(Lrows)


def residual_bound(Fivs: list[Interval], v: list[Fraction]) -> Fraction:
    vals = []
    for iv, vi in zip(Fivs, v):
        vals.append(maxabs_iv(sub_iv(iv, (vi, vi))))
    return max(vals)


def find_residual_certificate(cube, signed_T, a):
    v = eval_F_point(cube, signed_T, a)
    # Search coarse-to-fine.  r=h/10 forces localization much sharper than
    # absolute h*|F| propagation while remaining easy to audit exactly.
    for k in range(3, 13):
        h = Fraction(1, 10**k)
        r = h / 10
        X = affine_path_tube(a, v, h, r)
        Fivs, L = interval_F_and_L(cube, signed_T, X)
        R = residual_bound(Fivs, v)
        self_ratio = h * R / r
        q = h * L
        if self_ratio <= Fraction(1, 2) and q <= Fraction(1, 2):
            return {
                "h": h,
                "r": r,
                "v": v,
                "X": X,
                "R": R,
                "L": L,
                "self_ratio": self_ratio,
                "q": q,
            }
    raise AssertionError("no residual-centered certificate found in declared finite search")


def endpoint_box(a, v, h: Fraction, r: Fraction) -> list[Interval]:
    return [
        (
            Fraction(int(ai)) + h * vi - r,
            Fraction(int(ai)) + h * vi + r,
        )
        for ai, vi in zip(a, v)
    ]


def negative_control_constant_drift() -> dict:
    # Absolute symmetric propagation for x'=1, x(0)=0:
    # after n equal steps h=1/n to T=1, halfwidth is n*h=1 for every n.
    widths = []
    for n in (1, 10, 100, 1000):
        h = Fraction(1, n)
        halfwidth = n * h
        assert halfwidth == 1
        widths.append((n, halfwidth))

    # Residual path p(t)=t has p'=1=F(p), so R=0 and exact endpoint at T=1.
    residual = Fraction(0)
    endpoint_error = Fraction(0)
    assert residual == 0 and endpoint_error == 0
    return {
        "absolute_halfwidths": {str(n): str(w) for n, w in widths},
        "residual_reference_path": "p(t)=t",
        "residual_bound": "0",
        "endpoint_error": "0",
    }


def frac_text(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def main() -> int:
    neg = negative_control_constant_drift()

    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"]:
        raise RuntimeError("declared deterministic N=1 center did not reproduce")
    a = small.small_state(CENTER_SEED, cube.d)

    T = component.scaled_bilinear_tensor(cube)
    signed_T = signed_sparse_tensor(T)
    tensor_nonzero = sum(len(row) for row in signed_T)
    tensor_inf = max(sum(abs(coeff) for _, _, coeff in row) for row in signed_T)
    if tensor_nonzero != 2096 or tensor_inf != 36000:
        raise AssertionError("exact tensor audit drift")

    cert = find_residual_certificate(cube, signed_T, a)
    h = cert["h"]
    r = cert["r"]
    v = cert["v"]

    end = endpoint_box(a, v, h, r)
    mode_records = absolute.full_fourier_mode_records(cube, end)
    h3_status, h3_margin = h3.verdict(mode_records, H3_THRESHOLD)
    h3_lower = h3.h3_squared_lower(mode_records)
    if h3_status != "PASS":
        raise AssertionError("residual endpoint lost fixed H3 calibration witness")

    # Compare against an absolute enclosure at the same step on the same path/error
    # tube: absolute endpoint radius h*max|F|.  Residual centering must be sharper.
    Fivs, _ = interval_F_and_L(cube, signed_T, cert["X"])
    M_same = max(maxabs_iv(iv) for iv in Fivs)
    absolute_radius_same_h = h * M_same
    if not (r < absolute_radius_same_h):
        raise AssertionError("residual-centered endpoint did not improve localization")

    summary = {
        "negative_control": neg,
        "cutoff": 1,
        "dimension": cube.d,
        "center_seed": CENTER_SEED,
        "exact_tensor_nonzero_coefficients": tensor_nonzero,
        "exact_tensor_infinity_row_sum": tensor_inf,
        "h": frac_text(h),
        "residual_radius": frac_text(r),
        "residual_bound_R": frac_text(cert["R"]),
        "lipschitz_L": frac_text(cert["L"]),
        "self_map_ratio_hR_over_r": frac_text(cert["self_ratio"]),
        "contraction_q": frac_text(cert["q"]),
        "absolute_endpoint_radius_same_h": frac_text(absolute_radius_same_h),
        "localization_improvement_factor": frac_text(absolute_radius_same_h / r),
        "endpoint_H3_threshold": frac_text(H3_THRESHOLD),
        "endpoint_H3_squared_lower": frac_text(h3_lower),
        "endpoint_H3_margin": frac_text(h3_margin),
        "endpoint_H3_certificate": h3_status,
        "scope": (
            "fixed N=1 affine residual-tube calibration; exact finite arithmetic; "
            "no arbitrary-target termination, arbitrary-N constructor, or Clay conclusion"
        ),
    }
    print("NS-FUB-A1C N=1 residual-centered validated tube")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("NS-FUB-A1C N1 RESIDUAL TUBE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
