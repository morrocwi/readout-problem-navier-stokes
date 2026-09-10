#!/usr/bin/env python3
"""Energy-transfer observability bridge checks.

This checker validates finite algebra and explicit finite witnesses supporting the
bridge between shell-energy observability and EPSC. It deliberately keeps the
full EPSC-18/19 and all-N saturation claims OPEN.

Simulation=No for the modular/rational checks below; the boundary sweep is a
finite combinatorial diagnostic, not a continuum or all-N proof.
"""
from __future__ import annotations

import itertools
import json
from fractions import Fraction

import numpy as np

from check_volume6_ns_observability import CubeGalerkinModP, NU_MOD, P, rank_mod


def claim(cid, name, tier, status, evidence):
    return {"id": cid, "name": name, "tier": tier, "status": status, "evidence": evidence}


def boundary_witness(k, N):
    i = next(j for j, v in enumerate(k) if abs(v) == N)
    p = [0, 0, 0]
    if any(k[j] != 0 for j in range(3) if j != i):
        p[i] = 1 if k[i] > 0 else -1
    else:
        p[(i + 1) % 3] = 1
    p = tuple(p)
    q = tuple(k[j] - p[j] for j in range(3))
    cross = (
        p[1] * q[2] - p[2] * q[1],
        p[2] * q[0] - p[0] * q[2],
        p[0] * q[1] - p[1] * q[0],
    )
    ok = (
        max(abs(v) for v in p) <= N - 1
        and q != (0, 0, 0)
        and max(abs(v) for v in q) <= N
        and tuple(p[j] + q[j] for j in range(3)) == k
        and cross != (0, 0, 0)
    )
    return ok, p, q


def transfer_jet_rank_check():
    cube = CubeGalerkinModP()
    b0, b1 = cube.formal_shell_blocks(Rmax=1, seed=20260909)
    factors = np.asarray(
        [(2 * NU_MOD * int(s)) % P for s in cube.shells], dtype=np.int64
    )[:, None]
    transfer_block = (b1 + factors * b0) % P

    jet_rank = rank_mod(np.vstack((b0, b1)))
    transfer_rank = rank_mod(np.vstack((b0, transfer_block)))
    transfer_sum_gradient_zero = bool(np.all(np.sum(transfer_block, axis=0) % P == 0))

    return {
        "shells": cube.shells,
        "jet_rank": jet_rank,
        "energy_plus_transfer_rank": transfer_rank,
        "expected_first_block_ceiling": 5,
        "transfer_sum_gradient_zero": transfer_sum_gradient_zero,
        "pass": jet_rank == transfer_rank == 5 and transfer_sum_gradient_zero,
    }


def triad_quantitative_inverse_check():
    ca = Fraction(3, 10)
    nu = Fraction(1, 200)
    x = Fraction(1, 1)
    r = Fraction(1, 1)
    j = 2 * ca * r - 2 * nu * x

    dx = Fraction(1, 1000)
    dj = -Fraction(1, 2000)
    xhat = x + dx
    jhat = j + dj
    rhat = (jhat + 2 * nu * xhat) / (2 * ca)
    err = abs(rhat - r)
    bound = (abs(dj) + 2 * nu * abs(dx)) / (2 * abs(ca))
    return {
        "true_j1_a": str(j),
        "r_hat": str(rhat),
        "absolute_error": str(err),
        "certified_bound": str(bound),
        "closed_form_at_nu_1_over_200": "rho_r <= (5/3) sigma_J + (1/60) sigma_x",
        "pass": err <= bound,
    }


def boundary_connectivity_sweep(max_N=8):
    counts = {}
    all_ok = True
    for N in range(2, max_N + 1):
        boundary = 0
        passed = 0
        for k in itertools.product(range(-N, N + 1), repeat=3):
            if k == (0, 0, 0) or max(abs(v) for v in k) != N:
                continue
            boundary += 1
            ok, _, _ = boundary_witness(k, N)
            passed += int(ok)
            all_ok = all_ok and ok
        counts[N] = {"boundary_modes": boundary, "witnessed": passed}
    return {"through_N": max_N, "counts": counts, "pass": all_ok}


def window_radius_check():
    # Exact interval-radius propagation example:
    # rad(int T)=r1+r0+2 nu s rI+rF.
    r0 = Fraction(1, 100)
    r1 = Fraction(1, 50)
    rI = Fraction(3, 100)
    nu = Fraction(1, 10)
    s = 2
    rF = Fraction(0, 1)
    radius = r1 + r0 + 2 * nu * s * rI + rF
    return {"radius": str(radius), "expected": "21/500", "pass": radius == Fraction(21, 500)}


def main():
    claims = []

    rank = transfer_jet_rank_check()
    claims.append(claim(
        "V7-NSOBS-TRANSFER-JET-EQUIVALENCE",
        "shell transfer and first shell-energy jet carry the same local rank information",
        "finite_diagnostic",
        "PASS" if rank["pass"] else "FAIL",
        f"K=1 exact modular: rank(I,dI)={rank['jet_rank']}, rank(I,T)={rank['energy_plus_transfer_rank']}, sum_s D T_s=0={rank['transfer_sum_gradient_zero']}",
    ))

    triad = triad_quantitative_inverse_check()
    claims.append(claim(
        "V7-EPSC-18-TRIAD-QUANTITATIVE-INVERSE",
        "quantitative retained-state inverse radius in the analytic three-mode reduced subcase",
        "Dr",
        "DERIVED" if triad["pass"] else "FAIL",
        f"r error={triad['absolute_error']} <= bound={triad['certified_bound']}; this is a reduced-subcase witness, not the full N=1 cube",
    ))

    sweep = boundary_connectivity_sweep(8)
    claims.append(claim(
        "V7-NSOBS-ALL-N-TRIAD-CONNECTIVITY-LEMMA",
        "every new boundary mode has a constructive non-collinear triad connection to the previous cutoff",
        "Dr",
        "DERIVED" if sweep["pass"] else "FAIL",
        "analytic construction in reproduction/NS_ENERGY_TRANSFER_OBSERVABILITY_BRIDGE.md; exhaustive finite check through N=8=" + str(sweep["pass"]),
    ))

    window = window_radius_check()
    claims.append(claim(
        "V7-EPSC-19-WINDOW-TRANSFER-RADIUS",
        "integrated shell-transfer observable admits direct certified interval-radius propagation",
        "Dr",
        "DERIVED" if window["pass"] else "FAIL",
        f"sample exact radius={window['radius']}; removes numerical differentiation from this substep only",
    ))

    claims.append(claim(
        "V7-EPSC-18-FULL-CUBE-INVERSE",
        "full finite Fourier quotient-state certified inverse radius",
        "Open",
        "OPEN",
        "triad subcase is now quantitative, but full-cube gauge fixing, branch control and certified conditioning remain unresolved",
    ))
    claims.append(claim(
        "V7-EPSC-19-FULL-NOISY-INVERSE",
        "full noise-stable measurement-to-continuum certificate",
        "Open",
        "OPEN",
        "window transfer avoids derivative amplification for one observable layer; stable inversion to rho_N is still required",
    ))
    claims.append(claim(
        "V7-NSOBS-ALL-N-SATURATION-AFTER-CONNECTIVITY",
        "all-N earliest-order energy observability saturation",
        "Open",
        "OPEN",
        "kinematic transfer connectivity is closed; nonvanishing/algebraic independence of enough observable minors remains open",
    ))

    failed = [c for c in claims if c["status"] == "FAIL"]
    print("energy-transfer observability bridge")
    print("rank:", rank)
    print("triad inverse:", triad)
    print("boundary sweep:", sweep)
    print("window radius:", window)
    for c in claims:
        print(f"{c['id']}: {c['status']} -- {c['evidence']}")
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
