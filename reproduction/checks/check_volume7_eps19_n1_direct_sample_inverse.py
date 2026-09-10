#!/usr/bin/env python3
"""Direct raw-sample local inverse certificate for EPSC-19/EPSC-36 at fixed N=1.

This checker closes a deliberately local, finite-first measurement interface around the
already-certified small-integer N=1 observability center.  It does *not* reconstruct a
high-order Taylor jet from noisy samples.  Instead it builds a preconditioner for the
49-row finite-time sample map directly and certifies the actual finite Galerkin flow by
finite Taylor-remainder and integral-bootstrap bounds.

Sample map
----------
For the finite N=1 Galerkin flow phi_t and its three shell energies I_s, use

    S_h(x) = (
        I_0(phi_{jh}(x))  for j=0..23,
        I_1(phi_{jh}(x))  for j=0..23,
        I_2(x)
    )

on the explicit 49-dimensional translation slice.  The spacing is the explicit
rational h=10^-200.  This tiny value is chosen for proof robustness, not practical
sensing.

Direct preconditioner
---------------------
Let J_z be the exact integer 49x49 scaled Taylor-jet Jacobian in sample-channel order,
where z_{s,n}=C^n n! a_{s,n}, C=600.  For the degree-23 sample Jacobian polynomial,

    J_T(h) = P_h J_z,

with two Vandermonde blocks P_h = V diag(h^n/(C^n n!)) and one identity row.  The
checker constructs the exact rational direct-sample preconditioner

    A_h = J_z^{-1} P_h^{-1},

so A_h J_T(h)=I exactly.  This factorization is used only to construct A_h; noisy
samples are never converted into Taylor coefficients in the certified inverse theorem.

Validated finite flow/tangent enclosure
----------------------------------------
On the declared state box ||x||_inf<=4 over 0<=t<=23h, finite operator bounds verify by
integral bootstrap that the flow remains in the box, ||D phi_t||_inf<=2, and the second
variation norm is <=1.  A finite 24th-order Taylor theorem bounds the center sample
Jacobian remainder.  A finite 48th-order Taylor theorem bounds the center sample-value
remainder used for raw-data branch capture.  No infinite Fourier object and no
completed-infinity premise appears.

If e_j bounds the center Jacobian remainder row and H_j bounds the sample-map Hessian
row on a branch of radius r, then

    q <= max_i sum_j |A_h[i,j]| (e_j + r H_j).

The checker chooses r>0 so q<=1/2.  It then certifies a strictly positive raw-sample
margin delta such that any measured sample center y_obs with sensor radius sigma and

    ||y_obs - y_T||_inf + sigma <= delta

(where y_T is the exact degree-47 center sample polynomial) satisfies the contraction
self-map condition on the declared branch.  Hence every data vector in that raw sample
box has a unique solution in the certified local branch, and

    ||x-x_*||_inf <= ||A_h||_inf/(1-q) *
                     (||y_obs-y_T||_inf + sigma + tau_T),

with tau_T the certified degree-47 center-flow remainder.

Boundary: this is a fixed-N=1 local mathematical measurement certificate.  Its spacing
and admissible raw-sample tolerance are intentionally microscopic.  It does not claim a
practical sensor regime, global injectivity, arbitrary finite N, continuum regularity,
or a Clay result.  Those remain separate obligations.
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_exact_preconditioner as exact
import check_volume7_eps18_n1_explicit_radius as coarse
import check_volume7_eps18_n1_small_witness as small
import check_volume7_eps19_n1_sample_interpolation_conditioning as interp

C = 600
CENTER_SEED = 20260910
R_JAC = 23
R_VALUE = 47
H = Fraction(1, 10**200)
MAX_NODE = 23
BRANCH_CAP = Fraction(1, 1000)
STATE_BOUND = Fraction(4)
TANGENT_BOUND = Fraction(2)
SECOND_VARIATION_BOUND = Fraction(1)
Q_TARGET = Fraction(1, 2)


def matmul(A, B):
    rows = len(A)
    inner = len(B)
    cols = len(B[0])
    if any(len(row) != inner for row in A) or any(len(row) != cols for row in B):
        raise ValueError("incompatible matrices")
    out = [[Fraction(0) for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for k in range(inner):
            aik = A[i][k]
            if not aik:
                continue
            for j in range(cols):
                bkj = B[k][j]
                if bkj:
                    out[i][j] += aik * bkj
    return out


def identity_error(A, J):
    M = matmul(A, J)
    n = len(M)
    return max(
        sum((abs(M[i][j] - Fraction(int(i == j))) for j in range(n)), Fraction(0))
        for i in range(n)
    )


def weighted_row_norm(A, row_weights):
    if len(A[0]) != len(row_weights):
        raise ValueError("row weight length mismatch")
    return max(
        sum((abs(A[i][j]) * row_weights[j] for j in range(len(row_weights))), Fraction(0))
        for i in range(len(A))
    )


def power10_bracket(x: Fraction) -> str:
    p = interp.floor_log10_fraction(x)
    return f"10^{p} <= value < 10^{p + 1}"


def majorants_to(*, M: int, op: dict, order: int) -> dict:
    """Finite scaled time-derivative majorants through one declared finite order."""
    lc = int(op["Lc_bound"])
    bt = int(op["Btilde_bound"])
    qq = int(op["Q_bound"])
    a = [int(M)]
    b = [1]
    value = []
    first = []
    for n in range(order + 1):
        y0 = 0
        y1 = 0
        for i in range(n + 1):
            j = n - i
            w = math.comb(n, i)
            y0 += qq * w * a[i] * a[j]
            y1 += qq * w * (b[i] * a[j] + a[i] * b[j])
        value.append(y0)
        first.append(y1)
        if n == order:
            break
        an = lc * a[n]
        bn = lc * b[n]
        for i in range(n + 1):
            j = n - i
            w = math.comb(n, i)
            an += bt * w * a[i] * a[j]
            bn += bt * w * (b[i] * a[j] + a[i] * b[j])
        a.append(an)
        b.append(bn)
    return {"state": a, "first": b, "output_value": value, "output_first": first}


def exact_scaled_output_values(cube, x0_signed, order: int):
    """Return Y_n=C^n d^n I_s(phi_t(x0))/dt^n|_0 exactly, n=0..order."""
    x0 = np.asarray(x0_signed, dtype=object)
    X = [x0]
    W = np.asarray(cube.weights, dtype=object)
    outputs = []
    lc_diag = np.repeat(
        np.asarray([-3 * sum(int(v) * int(v) for v in k) for k in cube.reps], dtype=object),
        4,
    )
    for n in range(order + 1):
        y = np.zeros(len(cube.shells), dtype=object)
        for i in range(n + 1):
            j = n - i
            y += math.comb(n, i) * ((X[i] * X[j]) @ W.T)
        outputs.append([int(v) for v in y])
        if n == order:
            break
        rhs = X[n] * lc_diag
        for i in range(n + 1):
            j = n - i
            rhs += math.comb(n, i) * exact._scaled_bilinear(cube, X[i], X[j])
        X.append(rhs)
    return outputs


def build_direct_preconditioner(cube, x0, free):
    blocks = exact.exact_scaled_shell_blocks(cube, x0)
    rows = (
        [(0, n) for n in range(R_JAC + 1)]
        + [(1, n) for n in range(R_JAC + 1)]
        + [(2, 0)]
    )
    Jz = [[int(blocks[n][s, j]) for j in free] for s, n in rows]
    Jz_inv, det_jz = exact.exact_inverse(Jz)
    if det_jz == 0:
        raise ArithmeticError("scaled sample-order jet Jacobian is singular")

    vinv = interp.vandermonde_inverse_rows(tuple(range(R_JAC + 1)))
    Pinv = [[Fraction(0) for _ in range(49)] for _ in range(49)]
    for offset in (0, 24):
        for n in range(24):
            scale = Fraction(C**n * math.factorial(n), 1) / (H**n)
            for j in range(24):
                Pinv[offset + n][offset + j] = scale * vinv[n][j]
    Pinv[48][48] = Fraction(1)
    A = matmul(Jz_inv, Pinv)

    # Exact degree-23 sample Jacobian, used only to verify A J_T = I exactly.
    P = [[Fraction(0) for _ in range(49)] for _ in range(49)]
    nodes = tuple(range(24))
    for offset in (0, 24):
        for j, node in enumerate(nodes):
            for n in range(24):
                P[offset + j][offset + n] = Fraction(node**n, 1) * (H**n) / Fraction(C**n * math.factorial(n), 1)
    P[48][48] = Fraction(1)
    JT = matmul(P, Jz)
    return A, JT, det_jz


def center_value_polynomial(cube, x0):
    values = exact_scaled_output_values(cube, x0, R_VALUE)
    out = []
    for shell in (0, 1):
        for node in range(24):
            t = H * node
            acc = Fraction(0)
            for n in range(R_VALUE + 1):
                acc += Fraction(values[n][shell], C**n * math.factorial(n)) * (t**n)
            out.append(acc)
    out.append(Fraction(values[0][2], 1))
    return out


def main() -> int:
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"] or center["max_abs_coordinate"] > 3:
        raise RuntimeError("declared N=1 small-integer center did not reproduce")
    x0 = small.small_state(CENTER_SEED, cube.d)
    gauge = [int(v) for v in center["gauge_coordinates"]]
    free = [j for j in range(cube.d) if j not in gauge]
    if len(free) != 49:
        raise RuntimeError("expected 49-dimensional translation slice")

    op = coarse.finite_operator_bounds(cube)
    L = Fraction(op["Lc_bound"], C)
    B = Fraction(op["Btilde_bound"], C)
    Q = Fraction(op["Q_bound"])
    T = MAX_NODE * H

    # Finite integral bootstraps.  They validate the actual finite ODE flow and its
    # first two variations over the complete sampling window.
    initial_bound = Fraction(center["max_abs_coordinate"]) + BRANCH_CAP
    f_bound = L * STATE_BOUND + B * STATE_BOUND * STATE_BOUND
    k_bound = L + 2 * B * STATE_BOUND
    state_bootstrap = initial_bound + T * f_bound <= STATE_BOUND
    tangent_bootstrap = 1 + T * k_bound * TANGENT_BOUND <= TANGENT_BOUND
    second_bootstrap = T * (
        k_bound * SECOND_VARIATION_BOUND + 2 * B * TANGENT_BOUND * TANGENT_BOUND
    ) <= SECOND_VARIATION_BOUND
    flow_ok = bool(state_bootstrap and tangent_bootstrap and second_bootstrap)

    A, JT, det_jz = build_direct_preconditioner(cube, x0, free)
    exact_inverse_ok = identity_error(A, JT) == 0
    A_inf = weighted_row_norm(A, [Fraction(1) for _ in range(49)])

    # Finite 24th-order Taylor remainder for the center sample Jacobian.
    m24 = majorants_to(M=4, op=op, order=24)
    jac_d24 = Fraction(m24["output_first"][24], C**24) * TANGENT_BOUND
    jac_remainders = []
    for _shell in (0, 1):
        for node in range(24):
            t = H * node
            jac_remainders.append(jac_d24 * (t**24) / math.factorial(24))
    jac_remainders.append(Fraction(0))
    q_center = weighted_row_norm(A, jac_remainders)

    # Direct sample-map Hessian bound on the complete branch from the validated
    # flow/tangent/second-variation enclosure.
    H_sample = 2 * Q * (
        TANGENT_BOUND * TANGENT_BOUND + STATE_BOUND * SECOND_VARIATION_BOUND
    )
    hessian_rows = [H_sample for _ in range(49)]
    q_slope = weighted_row_norm(A, hessian_rows)
    if q_center >= Q_TARGET or q_slope <= 0:
        radius = Fraction(0)
    else:
        radius = min(BRANCH_CAP, (Q_TARGET - q_center) / q_slope)
    q_total = q_center + q_slope * radius if radius > 0 else Fraction(1)

    # Finite 48th-order Taylor theorem for actual center sample values.  Computing
    # the exact degree-47 polynomial makes the raw-data acceptance box explicit.
    center_poly = center_value_polynomial(cube, x0)
    if len(center_poly) != 49:
        raise RuntimeError("center sample polynomial must have 49 rows")
    m48 = majorants_to(M=4, op=op, order=48)
    value_d48 = Fraction(m48["output_value"][48], C**48)
    value_remainders = []
    for _shell in (0, 1):
        for node in range(24):
            t = H * node
            value_remainders.append(value_d48 * (t**48) / math.factorial(48))
    value_remainders.append(Fraction(0))
    tau_center = max(value_remainders)

    if radius > 0 and q_total < 1:
        inverse_factor = A_inf / (1 - q_total)
        branch_data_budget = (1 - q_total) * radius / A_inf
        raw_sensor_margin = branch_data_budget - tau_center
    else:
        inverse_factor = Fraction(0)
        branch_data_budget = Fraction(0)
        raw_sensor_margin = Fraction(-1)

    direct_ok = bool(
        flow_ok
        and det_jz != 0
        and exact_inverse_ok
        and q_center < Q_TARGET
        and radius > 0
        and q_total <= Q_TARGET
        and tau_center > 0
        and raw_sensor_margin > 0
    )

    claims = [
        {
            "id": "V7-EPSC19-N1-DIRECT-SAMPLE-FLOW-ENCLOSURE",
            "name": "validated finite N=1 flow/tangent enclosure over the explicit raw-sample window",
            "tier": "Dr",
            "status": "DERIVED" if flow_ok else "OPEN",
            "evidence": (
                f"h=10^-200; T=23h; state<=4 bootstrap={state_bootstrap}; "
                f"||Dphi||_inf<=2 bootstrap={tangent_bootstrap}; second variation<=1 bootstrap={second_bootstrap}"
            ),
        },
        {
            "id": "V7-EPSC19-N1-DIRECT-SAMPLE-PRECONDITIONER",
            "name": "exact rational preconditioner for the degree-23 direct 49-sample Jacobian",
            "tier": "finite_diagnostic",
            "status": "PASS" if det_jz != 0 and exact_inverse_ok else "FAIL",
            "evidence": (
                f"A_h=Jz^-1 P_h^-1 over Q; det(Jz)!=0; exact ||A_h J_T-I||_inf=0; "
                f"||A_h||_inf bracket: {power10_bracket(A_inf)}"
            ),
        },
        {
            "id": "V7-EPSC19-N1-DIRECT-SAMPLE-Q",
            "name": "branch-wide preconditioned Jacobian defect below one for the actual direct sample map",
            "tier": "Dr",
            "status": "DERIVED" if direct_ok else "OPEN",
            "evidence": (
                f"finite 24th-order center Jacobian remainder + validated Hessian variation; "
                f"q_center bracket={power10_bracket(q_center)}; chosen r bracket={power10_bracket(radius) if radius>0 else 'none'}; q_total<=1/2"
                if direct_ok else
                "direct sample-map flow/remainder/preconditioner conditions did not all certify"
            ),
        },
        {
            "id": "V7-EPSC19-N1-RAW-SAMPLE-BRANCH-CERTIFICATE",
            "name": "strictly positive raw-sample box certifies the fixed N=1 local inverse branch",
            "tier": "Dr",
            "status": "DERIVED" if direct_ok else "OPEN",
            "evidence": (
                f"degree-47 exact center sample polynomial with finite 48th-order remainder tau_T; "
                f"branch data budget {power10_bracket(branch_data_budget)}; tau_T {power10_bracket(tau_center)}; "
                f"remaining raw sample-center plus sensor margin {power10_bracket(raw_sensor_margin)}. "
                "Banach self-map/contraction: ||A_h||(data discrepancy)+q r<=r."
                if direct_ok else
                "no positive raw-data margin remained after certified center-flow remainder"
            ),
        },
        {
            "id": "V7-EPSC19-N1-RAW-SAMPLES-TO-RHO1",
            "name": "direct finite raw shell-energy samples propagate to a certified retained-state rho_1 on the validated branch",
            "tier": "Dr",
            "status": "DERIVED" if direct_ok else "OPEN",
            "evidence": (
                f"rho_1 <= ||A_h||/(1-q) * (sample-center discrepancy + sensor radius + tau_T); "
                f"inverse factor bracket {power10_bracket(inverse_factor)}; accepted data are certified to remain inside r"
                if direct_ok else
                "direct raw-sample inverse prerequisites did not all certify"
            ),
        },
        {
            "id": "V7-EPSC19-N1-PRACTICAL-DIRECT-SAMPLE-INVERSE",
            "name": "practically useful direct sample spacing and sensor tolerance for N=1",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "the explicit proof spacing h=10^-200 is intentionally microscopic and the positive raw-sample margin is mathematical, not practical; "
                "optimizing spacing/preconditioning and validating realistic sensor scales remains open"
            ),
        },
    ]

    summary = {
        "cutoff": 1,
        "slice_dimension": 49,
        "spacing_h": "10^-200",
        "max_sample_time": "23*10^-200",
        "sample_count": 49,
        "center_taylor_degree_for_jacobian": 23,
        "center_taylor_degree_for_sample_values": 47,
        "flow_bootstrap": {
            "state_bound": "4",
            "tangent_bound": "2",
            "second_variation_bound": "1",
            "certified": flow_ok,
        },
        "direct_preconditioner_norm": power10_bracket(A_inf),
        "center_jacobian_remainder_defect": power10_bracket(q_center),
        "certified_branch_radius": power10_bracket(radius) if radius > 0 else None,
        "q_bound": "1/2" if direct_ok else None,
        "center_sample_value_remainder": power10_bracket(tau_center),
        "raw_branch_data_budget": power10_bracket(branch_data_budget) if branch_data_budget > 0 else None,
        "positive_raw_sensor_margin": power10_bracket(raw_sensor_margin) if raw_sensor_margin > 0 else None,
        "inverse_factor": power10_bracket(inverse_factor) if inverse_factor > 0 else None,
        "what_closed": (
            "fixed-N=1 direct raw finite sample map: explicit spacing, validated finite flow/tangent enclosure, "
            "exact preconditioner, q<1, positive local branch-capture data box, and raw-sample-to-rho_1 propagation"
            if direct_ok else "not closed"
        ),
        "what_remains_open": (
            "practical spacing/sensor scale, global branch uniqueness, arbitrary finite N, outer EPSC scaling, continuum regularity/Clay"
        ),
        "finite_first_scope": "all state, sample, Taylor-remainder and contraction objects are finite; no completed N=infinity object is used",
    }
    print("EPSC-19 fixed-N=1 direct raw-sample inverse certificate")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims, "summary": summary}, separators=(",", ":")))
    return 0 if all(c["status"] != "FAIL" for c in claims) and direct_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
