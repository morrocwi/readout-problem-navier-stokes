#!/usr/bin/env python3
"""Volume-7 PROP-EPSC-15: exact continuous-time enclosure from an RK4 tape.

This checker closes the numerical-enclosure construction left open by the
relative-energy adapter. It does not prove the underlying Leray relative-
energy theorem (that remains analytic tier Dr) and it does not prove global
regularity.

Construction
------------
1. Generate a finite Fourier RK4 node tape in ordinary binary64 arithmetic.
2. Interpret every recorded real/imaginary component as its exact IEEE-754
   dyadic rational and apply the Leray projector in exact Fraction arithmetic.
3. Join consecutive projected nodes by a continuous piecewise-linear path
   v_h(t). The path is exactly divergence-free and K-supported.
4. On each time cell, v_h is affine in theta. Therefore the full projected
   Navier-Stokes residual is a degree-2 polynomial in theta, supported in the
   finite 2K cube. Its homogeneous H^-1 squared norm is degree 4 and is
   integrated exactly with Fractions.
5. Bound int ||grad v_h||_infinity dt using a rigorous Fourier l1 majorant,
   also in exact rational arithmetic.
6. Bound exp(A) from above by a rational Taylor/geometric remainder bound.
   Thus the terminal relative-energy beta^2 is an exact rational upper bound.

Norm convention: normalized 2*pi-periodic torus, so Parseval is
||u||_2^2 = sum_k |u_hat_k|^2 and
||r||_{H^-1}^2 = sum_{k != 0} |r_hat_k|^2/|k|^2.

Evidence tier for the finite enclosure computation: finite_diagnostic.
The continuum implication obtained by combining it with PROP-EPSC-13 is Dr.

[SimulatedData] Simulation=Yes
"""
from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from functools import lru_cache

import numpy as np

F = Fraction
Mode = tuple[int, int, int]
QComplex = tuple[Fraction, Fraction]
QVec = tuple[QComplex, QComplex, QComplex]
ZERO: QComplex = (F(0), F(0))


@lru_cache(maxsize=None)
def build_plan(K: int):
    modes = np.asarray(
        [k for k in itertools.product(range(-K, K + 1), repeat=3)
         if k != (0, 0, 0)],
        dtype=np.int64,
    )
    index = {tuple(map(int, k)): i for i, k in enumerate(modes)}
    out_idx, p_idx, q_idx = [], [], []
    for oi, karr in enumerate(modes):
        k = tuple(map(int, karr))
        for pi, parr in enumerate(modes):
            p = tuple(map(int, parr))
            q = tuple(k[j] - p[j] for j in range(3))
            qi = index.get(q)
            if qi is not None:
                out_idx.append(oi)
                p_idx.append(pi)
                q_idx.append(qi)
    return {
        "K": K,
        "modes": modes,
        "index": index,
        "out_idx": np.asarray(out_idx, dtype=np.int32),
        "p_idx": np.asarray(p_idx, dtype=np.int32),
        "q_idx": np.asarray(q_idx, dtype=np.int32),
        "k2": np.sum(modes * modes, axis=1).astype(np.float64),
    }


def leray_float(v: np.ndarray, modes: np.ndarray) -> np.ndarray:
    k2 = np.sum(modes * modes, axis=1).astype(np.float64)
    kv = np.sum(modes * v, axis=1)
    return v - modes * (kv / k2)[:, None]


def rhs_float(u: np.ndarray, nu: float, plan: dict) -> np.ndarray:
    qvec = plan["modes"][plan["q_idx"]]
    q_dot_up = np.sum(qvec * u[plan["p_idx"]], axis=1)
    terms = q_dot_up[:, None] * u[plan["q_idx"]]
    conv = np.zeros_like(u, dtype=np.complex128)
    np.add.at(conv, plan["out_idx"], terms)
    conv *= 1j
    conv = leray_float(conv, plan["modes"])
    return -conv - nu * plan["k2"][:, None] * u


def rk4_step_float(u: np.ndarray, dt: float, nu: float, plan: dict) -> np.ndarray:
    k1 = rhs_float(u, nu, plan)
    k2 = rhs_float(u + 0.5 * dt * k1, nu, plan)
    k3 = rhs_float(u + 0.5 * dt * k2, nu, plan)
    k4 = rhs_float(u + dt * k3, nu, plan)
    return u + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def taylor_green_state(plan: dict) -> np.ndarray:
    u = np.zeros((len(plan["modes"]), 3), dtype=np.complex128)
    for k in itertools.product((-1, 1), repeat=3):
        u[plan["index"][k]] = (-1j * k[0] / 8.0, 1j * k[1] / 8.0, 0.0)
    return u


def shear_state(plan: dict) -> np.ndarray:
    u = np.zeros((len(plan["modes"]), 3), dtype=np.complex128)
    u[plan["index"][(1, 0, 0)]] = (0.0, -0.5j, 0.0)
    u[plan["index"][(-1, 0, 0)]] = (0.0, 0.5j, 0.0)
    return u


def generate_tape(u0: np.ndarray, *, steps: int, dt: float, nu: float, plan: dict):
    tape = [u0.copy()]
    u = u0.copy()
    for _ in range(steps):
        u = rk4_step_float(u, dt, nu, plan)
        tape.append(u.copy())
    return tape


def qc(z: complex) -> QComplex:
    return (F.from_float(float(z.real)), F.from_float(float(z.imag)))


def cadd(a: QComplex, b: QComplex) -> QComplex:
    return (a[0] + b[0], a[1] + b[1])


def csub(a: QComplex, b: QComplex) -> QComplex:
    return (a[0] - b[0], a[1] - b[1])


def cscale(q: Fraction, a: QComplex) -> QComplex:
    return (q * a[0], q * a[1])


def cmul(a: QComplex, b: QComplex) -> QComplex:
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def ci(a: QComplex) -> QComplex:
    return (-a[1], a[0])


def re_a_conj_b(a: QComplex, b: QComplex) -> Fraction:
    return a[0] * b[0] + a[1] * b[1]


def vadd(a: QVec, b: QVec) -> QVec:
    return tuple(cadd(x, y) for x, y in zip(a, b))  # type: ignore[return-value]


def zero_vec() -> QVec:
    return (ZERO, ZERO, ZERO)


def exact_project(v: QVec, k: Mode) -> QVec:
    k2 = sum(x * x for x in k)
    if k2 == 0:
        return v
    dot = ZERO
    for ki, zi in zip(k, v):
        dot = cadd(dot, cscale(F(ki), zi))
    return tuple(
        csub(zi, cscale(F(ki, k2), dot))
        for ki, zi in zip(k, v)
    )  # type: ignore[return-value]


def rational_projected_node(arr: np.ndarray, modes: np.ndarray) -> list[QVec]:
    out = []
    for karr, row in zip(modes, arr):
        k = tuple(map(int, karr))
        out.append(exact_project(tuple(qc(z) for z in row), k))
    return out


def node_dict(node: list[QVec], modes: np.ndarray) -> dict[Mode, QVec]:
    return {tuple(map(int, k)): row for k, row in zip(modes, node)}


def node_divergence_exact(node: list[QVec], modes: np.ndarray) -> bool:
    for karr, row in zip(modes, node):
        s = ZERO
        for ki, zi in zip(map(int, karr), row):
            s = cadd(s, cscale(F(ki), zi))
        if s != ZERO:
            return False
    return True


def max_projection_correction_l1(float_node: np.ndarray, qnode: list[QVec]) -> Fraction:
    worst = F(0)
    for rowf, rowq in zip(float_node, qnode):
        for zf, zq in zip(rowf, rowq):
            d = csub(zq, qc(zf))
            worst = max(worst, abs(d[0]) + abs(d[1]))
    return worst


def convective_polynomial(a_node: list[QVec], b_node: list[QVec],
                          modes: np.ndarray) -> tuple[dict[Mode, list[QVec]], bool]:
    A = node_dict(a_node, modes)
    B = node_dict(b_node, modes)
    D = {
        k: tuple(csub(zb, za) for za, zb in zip(A[k], B[k]))
        for k in A
    }

    raw: dict[Mode, list[QVec]] = {}
    for p, ap in A.items():
        dp = D[p]
        for q, aq in A.items():
            dq = D[q]
            out = tuple(p[j] + q[j] for j in range(3))

            s0 = ZERO
            s1 = ZERO
            for qi, z0, z1 in zip(q, ap, dp):
                s0 = cadd(s0, cscale(F(qi), z0))
                s1 = cadd(s1, cscale(F(qi), z1))
            if s0 == ZERO and s1 == ZERO:
                continue

            c0 = tuple(ci(cmul(s0, z)) for z in aq)
            c1 = tuple(
                ci(cadd(cmul(s0, dz), cmul(s1, z)))
                for z, dz in zip(aq, dq)
            )
            c2 = tuple(ci(cmul(s1, dz)) for dz in dq)

            coeffs = raw.setdefault(out, [zero_vec(), zero_vec(), zero_vec()])
            coeffs[0] = vadd(coeffs[0], c0)  # type: ignore[arg-type]
            coeffs[1] = vadd(coeffs[1], c1)  # type: ignore[arg-type]
            coeffs[2] = vadd(coeffs[2], c2)  # type: ignore[arg-type]

    mean = raw.pop((0, 0, 0), [zero_vec(), zero_vec(), zero_vec()])
    mean_zero = all(z == ZERO for vec in mean for z in vec)
    projected = {
        k: [exact_project(vec, k) for vec in coeffs]
        for k, coeffs in raw.items()
    }
    return projected, mean_zero


def residual_polynomial(a_node: list[QVec], b_node: list[QVec],
                        modes: np.ndarray, *, h: Fraction, nu: Fraction
                        ) -> tuple[dict[Mode, list[QVec]], bool]:
    A = node_dict(a_node, modes)
    B = node_dict(b_node, modes)
    D = {
        k: tuple(csub(zb, za) for za, zb in zip(A[k], B[k]))
        for k in A
    }
    conv, mean_zero = convective_polynomial(a_node, b_node, modes)
    all_modes = set(conv) | set(A)
    residual: dict[Mode, list[QVec]] = {}

    for k in all_modes:
        coeffs = list(conv.get(k, [zero_vec(), zero_vec(), zero_vec()]))
        if k in A:
            k2 = sum(x * x for x in k)
            deriv = tuple(cscale(F(1, 1) / h, z) for z in D[k])
            visc0 = tuple(cscale(nu * k2, z) for z in A[k])
            visc1 = tuple(cscale(nu * k2, z) for z in D[k])
            coeffs[0] = vadd(coeffs[0], vadd(deriv, visc0))  # type: ignore[arg-type]
            coeffs[1] = vadd(coeffs[1], visc1)  # type: ignore[arg-type]
        residual[k] = coeffs

    return residual, mean_zero


def integrate_hminus1_squared_exact(residual: dict[Mode, list[QVec]],
                                    *, h: Fraction) -> Fraction:
    total = F(0)
    for k, coeffs in residual.items():
        k2 = sum(x * x for x in k)
        if k2 == 0:
            raise AssertionError("mean residual must vanish before H^-1 evaluation")
        for comp in range(3):
            c = [coeffs[j][comp] for j in range(3)]
            for a in range(3):
                for b in range(3):
                    total += (
                        h * re_a_conj_b(c[a], c[b])
                        / F(k2 * (a + b + 1))
                    )
    if total < 0:
        raise AssertionError("exact squared residual integral became negative")
    return total


def integrate_grad_linf_upper_exact(a_node: list[QVec], b_node: list[QVec],
                                    modes: np.ndarray, *, h: Fraction) -> Fraction:
    """Rigorous conservative bound on int ||grad v||_infinity dt.

    Operator norm <= sum_{i,j,k}|k_j||v_hat_{k,i}|; for complex z,
    |z| <= |Re z|+|Im z|. Convexity of absolute value then bounds the cell
    integral by the average of its endpoint l1 majorants.
    """
    total = F(0)
    for karr, arow, brow in zip(modes, a_node, b_node):
        k_l1 = sum(abs(int(x)) for x in karr)
        for za, zb in zip(arow, brow):
            ea = abs(za[0]) + abs(za[1])
            eb = abs(zb[0]) + abs(zb[1])
            total += F(k_l1) * h * (ea + eb) / 2
    return total


def exp_upper_rational(x: Fraction, *, N: int = 24) -> Fraction:
    """Exact rational upper bound for exp(x), x>=0."""
    if x < 0:
        raise ValueError("x must be nonnegative")
    term = F(1)
    partial = term
    for n in range(1, N + 1):
        term = term * x / n
        partial += term
    next_term = term * x / (N + 1)
    q = x / (N + 2)
    if q >= 1:
        raise ValueError("N too small for the geometric exponential tail bound")
    return partial + next_term / (1 - q)


def sqrt_upper_decimal_rational(x: Fraction, *, digits: int = 18) -> Fraction:
    """Ceiling of sqrt(x) on a decimal grid, using integer arithmetic only."""
    if x < 0:
        raise ValueError("x must be nonnegative")
    if x == 0:
        return F(0)
    D = 10 ** digits
    n = x.numerator * D * D
    q = x.denominator
    root_floor = math.isqrt(n // q)
    root_ceil = root_floor if root_floor * root_floor * q == n else root_floor + 1
    return F(root_ceil, D)


def certify_tape(float_tape: list[np.ndarray], modes: np.ndarray,
                 *, h: Fraction, nu: Fraction,
                 initial_error_sq: Fraction = F(0)) -> dict:
    qtape = [rational_projected_node(node, modes) for node in float_tape]
    divergence_ok = all(node_divergence_exact(node, modes) for node in qtape)
    projection_correction = max(
        max_projection_correction_l1(f, q)
        for f, q in zip(float_tape, qtape)
    )

    B = F(0)
    G = F(0)
    mean_zero = True
    for a, b in zip(qtape[:-1], qtape[1:]):
        residual, cell_mean_zero = residual_polynomial(a, b, modes, h=h, nu=nu)
        mean_zero = mean_zero and cell_mean_zero
        B += integrate_hminus1_squared_exact(residual, h=h)
        G += integrate_grad_linf_upper_exact(a, b, modes, h=h)

    A = 2 * G
    expA = exp_upper_rational(A)
    error_sq = expA * (initial_error_sq + B / nu)
    beta = sqrt_upper_decimal_rational(error_sq)

    return {
        "nodes": len(float_tape),
        "cells": len(float_tape) - 1,
        "exact_divergence_free_nodes": divergence_ok,
        "exact_zero_mean_residual": mean_zero,
        "max_projection_correction_l1": float(projection_correction),
        "A_upper": float(A),
        "B_hminus1_squared_time_integral_exact": float(B),
        "exp_A_upper": float(expA),
        "terminal_l2_error_squared_upper": float(error_sq),
        "terminal_l2_beta_decimal_upper": float(beta),
        "arithmetic": "exact fractions after binary64 tape capture",
    }


def run_shear_sanity() -> tuple[bool, dict]:
    plan = build_plan(1)
    h = F(1, 100)
    nu = F(1, 10)
    steps = 5
    tape = generate_tape(
        shear_state(plan), steps=steps, dt=float(h), nu=float(nu), plan=plan
    )
    cert = certify_tape(tape, plan["modes"], h=h, nu=nu)

    # Independent numerical sanity only: analytic shear solution is known.
    T = float(h * steps)
    exact_terminal = shear_state(plan) * math.exp(-float(nu) * T)
    actual_numeric_l2 = float(np.linalg.norm(tape[-1] - exact_terminal))
    cert["analytic_terminal_error_numeric_sanity"] = actual_numeric_l2
    ok = (
        cert["exact_divergence_free_nodes"]
        and cert["exact_zero_mean_residual"]
        and actual_numeric_l2 <= cert["terminal_l2_beta_decimal_upper"]
    )
    return bool(ok), cert


def run_taylor_green_certificate() -> tuple[bool, dict]:
    plan = build_plan(1)
    h = F(1, 100)
    nu = F(1, 100)
    steps = 5
    tape = generate_tape(
        taylor_green_state(plan), steps=steps, dt=float(h), nu=float(nu), plan=plan
    )
    cert = certify_tape(tape, plan["modes"], h=h, nu=nu)
    cert.update({
        "K": 1,
        "nu": float(nu),
        "dt": float(h),
        "T": float(h * steps),
        "modes": len(plan["modes"]),
        "ordered_retained_triads": len(plan["out_idx"]),
        "path": "exact-rational Leray-projected piecewise-linear interpolation of binary64 RK4 nodes",
        "norm_convention": "normalized 2*pi periodic torus",
    })
    ok = (
        cert["exact_divergence_free_nodes"]
        and cert["exact_zero_mean_residual"]
        and cert["B_hminus1_squared_time_integral_exact"] >= 0
        and math.isfinite(cert["terminal_l2_beta_decimal_upper"])
    )
    return bool(ok), cert


def main() -> int:
    shear_ok, shear = run_shear_sanity()
    tgv_ok, tgv = run_taylor_green_certificate()
    all_ok = shear_ok and tgv_ok

    claims = [
        {
            "id": "V7-EPSC-RK4-EXACT-PL-PATH",
            "name": "binary64 RK4 node tape admits an exact rational divergence-free piecewise-linear comparison path",
            "tier": "finite_diagnostic",
            "status": "PASS" if tgv_ok else "FAIL",
            "evidence": (
                f"K=1, nodes={tgv['nodes']}, exact divergence={tgv['exact_divergence_free_nodes']}, "
                f"projection correction L1={tgv['max_projection_correction_l1']:.3e}"
            ),
        },
        {
            "id": "V7-EPSC-RK4-CONTINUOUS-ENCLOSURE",
            "name": "validated continuous-time A_T/B_T enclosure from the floating-point RK4 tape",
            "tier": "finite_diagnostic",
            "status": "PASS" if tgv_ok else "FAIL",
            "evidence": (
                f"Abar={tgv['A_upper']:.12e}; B={tgv['B_hminus1_squared_time_integral_exact']:.12e}; "
                f"beta_upper={tgv['terminal_l2_beta_decimal_upper']:.12e}; exact Fraction arithmetic"
            ),
        },
        {
            "id": "V7-EPSC-RK4-SHEAR-SANITY",
            "name": "continuous-time enclosure dominates the known analytic shear terminal error",
            "tier": "finite_diagnostic",
            "status": "PASS" if shear_ok else "FAIL",
            "evidence": (
                f"beta={shear['terminal_l2_beta_decimal_upper']:.6e}; "
                f"analytic terminal error={shear['analytic_terminal_error_numeric_sanity']:.6e}"
            ),
        },
        {
            "id": "V7-EPSC-END2END-TERMINAL-ADAPTER",
            "name": "piecewise-linear tape enclosure combined with Leray relative energy yields a terminal L2/tail certificate",
            "tier": "Dr",
            "status": "DERIVED",
            "evidence": (
                "finite checker supplies rigorous Abar/Bbar for an exact comparison path; "
                "PROP-EPSC-13 supplies the standard analytic relative-energy implication"
            ),
        },
    ]

    print("Volume 7 -- exact RK4 continuous-time enclosure")
    print("[SimulatedData] Simulation=Yes")
    print("shear:", json.dumps(shear, sort_keys=True))
    print("taylor-green:", json.dumps(tgv, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
