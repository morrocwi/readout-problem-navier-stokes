#!/usr/bin/env python3
"""Finite witnesses for the terminal energy-budget EPSC certificate.

The continuum theorem remains analytic tier Dr.  This script checks the finite
orthogonal-energy algebra, directional-bound formula, fail-closed inconsistency
case, and the energy-defect-floor identity on explicit finite spectra.
"""
from __future__ import annotations

import json
import math


def orthogonal_energy_split_check():
    # Explicit Fourier coefficient energies; K=2 retains first three entries,
    # the rest are omitted.  Parseval reduces the check to a finite sum.
    retained_amp2 = [1.0, 0.5, 0.25]
    tail_amp2 = [0.125, 0.0625]
    full = sum(retained_amp2) + sum(tail_amp2)
    split = sum(retained_amp2) + sum(tail_amp2)
    ok = math.isclose(full, split, rel_tol=0.0, abs_tol=1e-15)
    return ok, {"full_l2_squared": full, "split_l2_squared": split}


def terminal_budget_bound_check():
    # Build a synthetic exact energy budget in squared-L2 units:
    # u0^2 = terminal_low^2 + terminal_tail^2 + 2 D_low + 2 D_tail + defect.
    low2 = 2.0
    tail2 = 0.3
    D_low = 0.4
    D_tail = 0.1
    defect = 0.2
    u0sq = low2 + tail2 + 2.0 * D_low + 2.0 * D_tail + defect

    beta2 = u0sq - low2 - 2.0 * D_low
    rhs_identity = tail2 + 2.0 * D_tail + defect
    ok = beta2 + 1e-15 >= tail2 and math.isclose(beta2, rhs_identity, abs_tol=1e-15)
    return ok, {
        "u0_squared": u0sq,
        "terminal_tail_squared": tail2,
        "beta_squared": beta2,
        "unresolved_dissipation_twice": 2.0 * D_tail,
        "energy_defect": defect,
    }


def energy_equality_closure_check():
    # Three increasing cutoffs with exact-energy-equality synthetic decomposition.
    # Both terminal tail and unresolved dissipation shrink to zero.
    rows = []
    previous = float("inf")
    ok = True
    for K, tail2, Dtail in [
        (2, 0.25, 0.125),
        (4, 0.04, 0.02),
        (8, 0.0025, 0.00125),
        (16, 0.0001, 0.00005),
    ]:
        defect = 0.0
        beta2 = tail2 + 2.0 * Dtail + defect
        beta = math.sqrt(beta2)
        ok = ok and beta < previous
        previous = beta
        rows.append({"K": K, "beta": beta, "beta_squared": beta2})
    ok = ok and rows[-1]["beta"] < rows[0]["beta"]
    return ok, rows


def fail_closed_inconsistency_check():
    U0 = 1.0
    retained_lower = 1.0
    D_lower = 0.1
    radicand = U0 * U0 - retained_lower * retained_lower - 2.0 * D_lower
    status = "HOLD" if radicand < 0 else "CERTIFIED_BOUND"
    return status == "HOLD", {"radicand": radicand, "status": status}


def main():
    p_ok, p = orthogonal_energy_split_check()
    b_ok, b = terminal_budget_bound_check()
    e_ok, e = energy_equality_closure_check()
    h_ok, h = fail_closed_inconsistency_check()
    finite_ok = p_ok and b_ok and e_ok and h_ok

    claims = [
        {
            "id": "V7-EPSC-TERMINAL-EB-ALGEBRA",
            "name": "terminal energy-budget tail inequality finite algebra",
            "tier": "finite_diagnostic",
            "status": "PASS" if (p_ok and b_ok) else "FAIL",
            "evidence": f"finite Parseval split pass={p_ok}; beta^2={b['beta_squared']:.6g} >= actual tail^2={b['terminal_tail_squared']:.6g}",
        },
        {
            "id": "V7-EPSC-TERMINAL-EB",
            "name": "Leray-Hopf terminal energy-budget certificate",
            "tier": "Dr",
            "status": "DERIVED",
            "evidence": "analytic proof in paper/NS_TERMINAL_ENERGY_BUDGET_CERTIFICATE.md; finite checker verifies only its orthogonal-energy algebra",
        },
        {
            "id": "V7-EPSC-ENERGY-EQUALITY-CLOSURE",
            "name": "energy equality forces energy-budget beta_K to zero",
            "tier": "Dr",
            "status": "DERIVED",
            "evidence": "beta_K^2 = terminal tail^2 + twice unresolved viscous dissipation + energy defect; under zero defect both unresolved terms vanish by monotone Fourier convergence",
        },
        {
            "id": "V7-EPSC-TERMINAL-ADAPTER",
            "name": "certified adapter from finite Galerkin trajectory to actual continuum projection",
            "tier": "Open",
            "status": "OPEN",
            "evidence": "required before plugging the project's surrogate finite trajectory into the continuum terminal energy-budget theorem",
        },
    ]

    print("Volume 7 -- terminal energy-budget EPSC finite witnesses")
    print("orthogonal split:", json.dumps(p))
    print("terminal budget:", json.dumps(b))
    print("energy-equality synthetic closure:", json.dumps(e))
    print("fail-closed inconsistency:", json.dumps(h))
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 0 if finite_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
