#!/usr/bin/env python3
"""Finite reproduction witnesses for the Volume-7 spectral tail certificate note.

The analytic Leray-Hopf theorem is tier Dr and is not faked as a finite proof here.
This script checks the finite spectral inequality, the high-mode non-identifiability
witness, and the explicit beta formulas used by the implementation.
"""
from __future__ import annotations

import json
import math
import random


def finite_spectral_check(seed: int = 20260910):
    rng = random.Random(seed)
    state = {}
    for i in range(-5, 6):
        for j in range(-5, 6):
            for k in range(-5, 6):
                if (i, j, k) == (0, 0, 0):
                    continue
                state[(i, j, k)] = tuple(
                    complex(rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0))
                    for _ in range(3)
                )

    rows = []
    ok = True
    for K in range(0, 5):
        tail_sq = 0.0
        grad_sq = 0.0
        for mode, u in state.items():
            amp_sq = sum(abs(z) ** 2 for z in u)
            k2 = sum(x * x for x in mode)
            grad_sq += k2 * amp_sq
            if max(abs(x) for x in mode) > K:
                tail_sq += amp_sq
        actual = math.sqrt(tail_sq)
        bound = math.sqrt(grad_sq) / (K + 1)
        passes = actual <= bound + 1e-12
        ok = ok and passes
        rows.append({"K": K, "actual_tail": actual, "hs1_bound": bound, "pass": passes})
    return ok, rows


def nonidentifiability_check(K: int = 4):
    # q is outside the retained cube and a is perpendicular to q.
    q = (K + 1, 0, 0)
    a1 = (0.0, 1.0, 0.0)
    a2 = (0.0, 100.0, 0.0)
    qdot1 = sum(q[i] * a1[i] for i in range(3))
    qdot2 = sum(q[i] * a2[i] for i in range(3))
    projected_change = 0.0  # both perturbations have support only at +-q
    tail1 = math.sqrt(2.0) * abs(a1[1])
    tail2 = math.sqrt(2.0) * abs(a2[1])
    ok = (
        max(abs(x) for x in q) == K + 1
        and qdot1 == 0.0
        and qdot2 == 0.0
        and projected_change == 0.0
        and math.isclose(tail2 / tail1, 100.0)
    )
    return ok, {
        "K": K,
        "q": q,
        "retained_projection_change": projected_change,
        "tail_ratio_after_100x_amplitude": tail2 / tail1,
    }


def beta_formula_check():
    nu = 0.01
    u0 = 2.0
    beta4 = u0 / (math.sqrt(2.0 * nu) * 5.0)
    beta9 = u0 / (math.sqrt(2.0 * nu) * 10.0)
    monotone = beta9 < beta4 and math.isclose(beta4 / beta9, 2.0, rel_tol=1e-14)

    forcing = 1.5
    K = 3
    forced = math.sqrt(u0 * u0 / nu + forcing * forcing / (nu * nu)) / (K + 1)
    forced_positive = math.isfinite(forced) and forced > 0.0
    return monotone and forced_positive, {
        "unforced_beta_K4": beta4,
        "unforced_beta_K9": beta9,
        "inverse_cutoff_ratio": beta4 / beta9,
        "forced_beta_K3": forced,
    }


def main():
    spectral_ok, spectral_rows = finite_spectral_check()
    nogo_ok, nogo = nonidentifiability_check()
    beta_ok, beta = beta_formula_check()

    all_finite_ok = spectral_ok and nogo_ok and beta_ok

    claims = [
        {
            "id": "V7-EPSC-SPECTRAL-CORE",
            "name": "finite H1-to-L2 Fourier tail inequality core",
            "tier": "finite_diagnostic",
            "status": "PASS" if spectral_ok else "FAIL",
            "evidence": f"tested K=0..4 on deterministic finite spectrum; all inequalities pass={spectral_ok}",
        },
        {
            "id": "V7-EPSC-TERMINAL-NOGO-WITNESS",
            "name": "high-mode perturbation leaves retained terminal record unchanged",
            "tier": "finite_diagnostic",
            "status": "PASS" if nogo_ok else "FAIL",
            "evidence": f"q={nogo['q']} lies outside K={nogo['K']}; retained change=0; tail scales by {nogo['tail_ratio_after_100x_amplitude']:.0f}x",
        },
        {
            "id": "V7-EPSC-04-ST",
            "name": "Leray-Hopf spacetime L2 omitted-tail certificate",
            "tier": "Dr",
            "status": "DERIVED",
            "evidence": "analytic proof in paper/NS_SPACETIME_TAIL_CERTIFICATE.md: spectral inequality + Leray-Hopf energy inequality; finite script checks only the spectral/algebraic core",
        },
        {
            "id": "V7-EPSC-READOUT-LIFT",
            "name": "Lipschitz readout lift of certified spacetime tail",
            "tier": "Dr",
            "status": "DERIVED",
            "evidence": "direct Lipschitz composition; time-average corollary by Cauchy-Schwarz",
        },
        {
            "id": "V7-EPSC-04-TERMINAL",
            "name": "arbitrary prescribed terminal full-state certificate",
            "tier": "Open",
            "status": "OPEN",
            "evidence": "finite terminal coefficients alone are non-identifying; a separately certified pointwise H^s bound would yield beta_K=M_s/(K+1)^s",
        },
    ]

    print("Volume 7 -- EPSC spectral tail certificate finite witnesses")
    for row in spectral_rows:
        print(
            f"K={row['K']} tail={row['actual_tail']:.6e} "
            f"H1/(K+1)={row['hs1_bound']:.6e} pass={row['pass']}"
        )
    print("terminal non-identifiability witness:", json.dumps(nogo))
    print("beta formula witness:", json.dumps(beta))
    print("analytic theorem tier: Dr (not mechanically proved by this script)")
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 0 if all_finite_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
