#!/usr/bin/env python3
"""Derivative-free finite-time sample-chart bridge for EPSC-19 at fixed N=1.

The existing N=1 shell-energy Taylor chart uses 49 independent rows on the explicit
49-dimensional translation slice: all three shell rows at Taylor order 0 and the
first two shell rows at every order 1..23.

This checker converts that *structural* jet statement into a derivative-free
finite-time sampling statement.

Let phi_t be the local analytic flow of the finite N=1 polynomial Galerkin ODE and
write, for shell s,

    I_s(phi_t(x)) = sum_{n>=0} a_{s,n}(x) t^n.

The existing modular checker computes D a_{s,n}(x_*).  Consider the 49-sample map

    S_h(x) = (
        I_0(phi_{0h}(x)), ..., I_0(phi_{23h}(x)),
        I_1(phi_{0h}(x)), ..., I_1(phi_{23h}(x)),
        I_2(x)
    ).

On the translation slice, det D S_h(x_*) is analytic in h.  Multilinearity of the
determinant and the 24x24 Vandermonde matrix at nodes 0,...,23 show

    det D S_h(x_*) = c h^552 + O(h^553),

where

    c = det(V)^2 det(J_jet),
    V[j,n] = j^n,  j,n=0,...,23,

and J_jet is the same 49-row Taylor-coefficient Jacobian, only reordered by shell.
Because both determinants are nonzero, c is nonzero.  Therefore there exists eta>0
such that every sufficiently small nonzero |h|<eta gives a locally invertible
*finite-time sample chart* on the same finite quotient slice.

This removes high-order numerical differentiation from the structural observability
interface.  It does NOT provide an explicit useful eta, a conditioned inverse factor,
noise tolerance, branch capture from raw sensors, arbitrary-N extension, continuum
regularity, or a Clay result.  Those remain separate fail-closed obligations.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_local_inverse as local
import check_volume7_eps18_n1_small_witness as small

P = base.P
CENTER_SEED = 20260910
RMAX = 23
SAMPLE_NODES = tuple(range(RMAX + 1))
LEADING_POWER = 2 * sum(SAMPLE_NODES)  # two 24-row shell blocks = 552


def vandermonde_mod(nodes: tuple[int, ...]) -> np.ndarray:
    return np.asarray(
        [[pow(int(t), n, P) for n in range(len(nodes))] for t in nodes],
        dtype=np.int64,
    ) % P


def vandermonde_product_mod(nodes: tuple[int, ...]) -> int:
    out = 1
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            out = (out * (int(nodes[j]) - int(nodes[i]))) % P
    return int(out)


def main() -> int:
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"]:
        raise RuntimeError("declared N=1 small-integer observability center did not reproduce")

    x0 = small.small_state(CENTER_SEED, cube.d)
    blocks = small.formal_shell_blocks_from_state(cube, x0)
    if len(blocks) != RMAX + 1 or len(cube.shells) != 3:
        raise RuntimeError("checker is scoped to the N=1 three-shell Taylor chart through order 23")

    gauge = [int(v) for v in center["gauge_coordinates"]]
    free = [j for j in range(cube.d) if j not in gauge]
    if len(free) != 49:
        raise RuntimeError("declared translation slice must have dimension 49")

    # Order rows exactly as the sample map: shell 0 at n=0..23, then shell 1,
    # then shell 2 at n=0.  This is a row permutation of the previously selected
    # chart [all shells at n=0; shell 0/1 at n=1..23].
    jet_pairs = (
        [(0, n) for n in range(RMAX + 1)]
        + [(1, n) for n in range(RMAX + 1)]
        + [(2, 0)]
    )
    J_jet = np.vstack([blocks[n][s, free] for s, n in jet_pairs]) % P
    jet_rank = base.rank_mod(J_jet)
    jet_det = int(local.det_mod(J_jet))

    selected_expected = [0, 1, 2]
    for n in range(1, RMAX + 1):
        selected_expected.extend([3 * n, 3 * n + 1])
    selected_actual = [int(v) for v in center["selected_observation_rows"]]
    row_pattern_ok = selected_actual == selected_expected

    V = vandermonde_mod(SAMPLE_NODES)
    v_rank = base.rank_mod(V)
    v_det = int(local.det_mod(V))
    v_det_formula = vandermonde_product_mod(SAMPLE_NODES)
    vandermonde_ok = v_rank == 24 and v_det != 0 and v_det == v_det_formula

    leading_coefficient_mod_p = (jet_det * v_det * v_det) % P
    leading_nonzero = bool(jet_rank == 49 and jet_det != 0 and vandermonde_ok and leading_coefficient_mod_p != 0)
    structural_ok = bool(center["pass"] and row_pattern_ok and leading_nonzero and LEADING_POWER == 552)

    claims = [
        {
            "id": "V7-EPSC19-N1-FINITE-SAMPLE-CHART-LEADING-COEFFICIENT",
            "name": "finite N=1 sample-time Jacobian has a nonzero h^552 leading determinant coefficient",
            "tier": "finite_diagnostic",
            "status": "PASS" if structural_ok else "FAIL",
            "evidence": (
                f"slice_dim=49; jet_rank={jet_rank}; jet_det_mod_p={jet_det}; "
                f"Vandermonde_rank={v_rank}; Vandermonde_det_mod_p={v_det}; "
                f"leading_coeff_mod_p={leading_coefficient_mod_p}; leading_power={LEADING_POWER}; "
                f"selected_row_pattern={row_pattern_ok}"
            ),
        },
        {
            "id": "V7-EPSC19-N1-DERIVATIVE-FREE-SAMPLE-CHART-EXISTENCE",
            "name": "sufficiently short nonzero finite sample spacing yields a local N=1 quotient chart without numerical differentiation",
            "tier": "Dr",
            "status": "DERIVED" if structural_ok else "OPEN",
            "evidence": (
                "for S_h=(I0(phi_jh))_{j=0..23}+(I1(phi_jh))_{j=0..23}+I2(x), "
                "analytic finite-ODE flow and determinant multilinearity give det D S_h(x*)="
                "c h^552+O(h^553) with c!=0; hence some eta>0 exists such that 0<|h|<eta is locally invertible"
                if structural_ok else
                "the finite nonzero leading-coefficient prerequisites did not reproduce"
            ),
        },
        {
            "id": "V7-EPSC19-N1-EXPLICIT-SAMPLE-SPACING-CONDITIONING",
            "name": "explicit finite sample spacing with certified branch-wide q_h<1 and useful noise factor",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "the h^552 theorem is existential as h->0; an explicit h must still balance validated flow/Taylor remainder "
                "against Vandermonde conditioning and certify a branch-wide preconditioned Jacobian defect"
            ),
        },
        {
            "id": "V7-EPSC19-N1-RAW-SENSOR-BRANCH-CAPTURE",
            "name": "raw noisy shell-energy samples select and remain in the certified local inverse branch",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "finite-time local observability no longer requires numerical differentiation, but sensor error, model discrepancy, "
                "explicit sample spacing, reconstruction residual, and branch selection still require a quantitative certificate"
            ),
        },
    ]

    summary = {
        "cutoff": 1,
        "state_dimension": cube.d,
        "slice_dimension": len(free),
        "shells": [int(s) for s in cube.shells],
        "sample_shells": [int(cube.shells[0]), int(cube.shells[1])],
        "sample_nodes_in_units_of_h": list(SAMPLE_NODES),
        "sample_count": 49,
        "time_samples_per_primary_shell": 24,
        "extra_shell2_sample_at_t0": 1,
        "max_taylor_order_used_for_leading_term": RMAX,
        "leading_power_h": LEADING_POWER,
        "prime": P,
        "jet_det_mod_p": jet_det,
        "vandermonde_det_mod_p": v_det,
        "leading_coefficient_mod_p": int(leading_coefficient_mod_p),
        "finite_first_scope": "fixed N=1 finite Galerkin flow and 49-dimensional translation slice",
        "what_closed": "structural existence of a derivative-free finite-time local sample chart for sufficiently small nonzero h",
        "what_remains_open": "explicit h, conditioning/noise factor, validated flow remainder over a branch, raw-sensor branch capture, arbitrary finite N, continuum adapter",
    }

    print("EPSC-19 fixed-N=1 finite-time sample-chart bridge")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 0 if structural_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
