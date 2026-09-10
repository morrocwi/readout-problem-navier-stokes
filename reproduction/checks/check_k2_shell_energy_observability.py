#!/usr/bin/env python3
"""Exact N=2 shell-energy observability saturation witness over F_251.

This closes the missing finite-resolution bridge between the already-certified
N=1 shell reader and N=3 shell reader.  The cubic cutoff K_2 has 124 nonzero
modes and 248 real incompressible degrees of freedom.  Translation symmetry
caps generic local shell-energy-jet rank at 245.  There are 9 exact |k|^2
shells, and nonlinear energy conservation gives one scalar dependence in every
new shell block, so

    rank D J_R <= min(9 + 8 R, 245).

Therefore R=30 is the earliest structurally possible order for saturation.  We
reuse the exact finite-field Galerkin/tangent machinery from the independent
N=2 scalar-energy checker, replace its scalar reader by all nine shell-energy
rows, and test the projected 245-column Jacobian exactly modulo p=251.

A final rank 245 at R=30 proves a nonzero characteristic-zero maximal minor for
this finite polynomial observation map.  Together with the translation upper
bound it gives generic local completeness modulo translations at this fixed
finite resolution.  It is not an arbitrary-N theorem, global inverse theorem,
continuum regularity result, DNS validation, or Clay claim.
"""
from __future__ import annotations

import json
import time
import numpy as np

import check_k2_energy_observability as k2

P = k2.P
RMAX = 30
BATCH = k2.d - 3
SEED_STATE = k2.SEED_STATE
SEED_PROJ = 20260913


@k2.njit(parallel=True, cache=True)
def shell_block(n, Vcoef, xcoef, weights, P):
    batch = Vcoef.shape[1]
    ns = weights.shape[0]
    out = np.empty((ns, batch), dtype=np.uint16)
    for bb in k2.prange(batch):
        for s in range(ns):
            acc = np.int64(0)
            for i in range(n + 1):
                j = n - i
                for c in range(Vcoef.shape[2]):
                    acc += (
                        2
                        * np.int64(weights[s, c])
                        * np.int64(Vcoef[i, bb, c])
                        * np.int64(xcoef[j, c])
                    )
            out[s, bb] = acc % P
    return out


def main() -> int:
    ns = len(k2.shells)
    ceiling = k2.d - 3
    assert k2.N == 2
    assert k2.d == 248 and k2.nm == 124 and BATCH == 245
    assert ns == 9 and k2.shells == [1, 2, 3, 4, 5, 6, 8, 9, 12]
    assert P == 251 and P > RMAX

    structural = lambda R: min(ns + (ns - 1) * R, ceiling)
    earliest = (ceiling - ns + (ns - 2)) // (ns - 1)
    assert earliest == 30 and structural(29) == 241 and structural(30) == 245

    print(
        f"N=2 shell-energy exact modular test: modes={k2.nm} d={k2.d} "
        f"shells={ns} prime={P} batch={BATCH} threads={k2.get_num_threads()}",
        flush=True,
    )
    print("shells=", k2.shells, flush=True)

    rng = np.random.default_rng(SEED_STATE)
    xcoef = np.zeros((RMAX + 1, k2.d), dtype=np.uint16)
    Ux = np.zeros((RMAX + 1, k2.nm, 3, 2), dtype=np.uint16)
    xcoef[0] = rng.integers(1, P, size=k2.d, dtype=np.uint16)
    k2.recon_one(xcoef[0], Ux[0], k2.full_rep, k2.full_sign, k2.E1u, k2.E2u, P)
    _ = k2.state_rhs(
        0, xcoef, Ux, k2.linu, k2.starts, k2.tp, k2.tq, k2.modes_arr,
        k2.reps_arr, k2.E1u, k2.E2u, k2.invn1u, k2.invn2u, k2.invk2u, P,
    )
    t0 = time.time()
    for n in range(RMAX):
        rhs = k2.state_rhs(
            n, xcoef, Ux, k2.linu, k2.starts, k2.tp, k2.tq, k2.modes_arr,
            k2.reps_arr, k2.E1u, k2.E2u, k2.invn1u, k2.invn2u, k2.invk2u, P,
        )
        xcoef[n + 1] = (rhs.astype(np.int64) * pow(n + 1, -1, P) % P).astype(np.uint16)
        k2.recon_one(xcoef[n + 1], Ux[n + 1], k2.full_rep, k2.full_sign, k2.E1u, k2.E2u, P)
    state_sec = time.time() - t0

    rng = np.random.default_rng(SEED_PROJ)
    Vcoef = np.zeros((RMAX + 1, BATCH, k2.d), dtype=np.uint16)
    UV = np.zeros((RMAX + 1, BATCH, k2.nm, 3, 2), dtype=np.uint16)
    Vcoef[0] = rng.integers(0, P, size=(BATCH, k2.d), dtype=np.uint16)
    k2.recon_batch(Vcoef[0], UV[0], k2.full_rep, k2.full_sign, k2.E1u, k2.E2u, P)
    _ = k2.tangent_rhs(
        0, Vcoef, UV, Ux, k2.linu, k2.starts, k2.tp, k2.tq, k2.modes_arr,
        k2.reps_arr, k2.E1u, k2.E2u, k2.invn1u, k2.invn2u, k2.invk2u, P,
    )

    weights = k2.weights.astype(np.uint16)
    blocks = [shell_block(0, Vcoef, xcoef, weights, P)]
    milestones = {0: k2.rank_mod(blocks[0])}
    t1 = time.time()
    for n in range(RMAX):
        rhs = k2.tangent_rhs(
            n, Vcoef, UV, Ux, k2.linu, k2.starts, k2.tp, k2.tq, k2.modes_arr,
            k2.reps_arr, k2.E1u, k2.E2u, k2.invn1u, k2.invn2u, k2.invk2u, P,
        )
        Vcoef[n + 1] = (rhs.astype(np.int64) * pow(n + 1, -1, P) % P).astype(np.uint16)
        k2.recon_batch(Vcoef[n + 1], UV[n + 1], k2.full_rep, k2.full_sign, k2.E1u, k2.E2u, P)
        blocks.append(shell_block(n + 1, Vcoef, xcoef, weights, P))
        R = n + 1
        if R in (1, 5, 10, 20, 25, 29, 30):
            A = np.vstack(blocks)
            rk = k2.rank_mod(A)
            milestones[R] = rk
            print(
                f"R={R} rank={rk} structural_ceiling={structural(R)} "
                f"rows={A.shape[0]} elapsed={time.time()-t1:.1f}s",
                flush=True,
            )

    A = np.vstack(blocks)
    final_rank = k2.rank_mod(A)
    saturation = final_rank == ceiling
    earliest_saturation = saturation and milestones.get(29, -1) < ceiling

    claims = [
        {
            "id": "V7-NSOBS-N2-SHELL-STRUCTURAL-BOUND",
            "name": "N=2 shell-energy reader cannot reach the translation ceiling before R=30",
            "tier": "Dr",
            "status": "DERIVED",
            "evidence": "d_2=248, m_2=9, translation ceiling=245, rank<=min(9+8R,245), hence R_min=30",
        },
        {
            "id": "V7-NSOBS-N2-SHELL-SATURATION",
            "name": "exact N=2 shell-energy jet reaches generic translation-limited rank 245 at R=30",
            "tier": "finite_diagnostic",
            "status": "PASS" if saturation else "FAIL",
            "evidence": f"exact F_251 projected Jacobian rank at R=30 is {final_rank}; target=245",
        },
        {
            "id": "V7-NSOBS-N2-SHELL-EARLIEST-SATURATION",
            "name": "N=2 shell-energy saturation occurs at the earliest structurally admissible order",
            "tier": "Dr",
            "status": "DERIVED" if earliest_saturation else "OPEN",
            "evidence": (
                f"R=29 rank={milestones.get(29)}<245 and R=30 rank={final_rank}=245"
                if earliest_saturation else
                "final exact saturation/earliest-order gate did not both certify"
            ),
        },
        {
            "id": "V7-NSOBS-SHELL-N123-CONTIGUOUS",
            "name": "shell-energy earliest-order saturation is now exactly witnessed at N=1,2,3",
            "tier": "Dr",
            "status": "DERIVED" if earliest_saturation else "OPEN",
            "evidence": (
                "combine existing N=1 R=23 and N=3 R=39 certificates with this exact N=2 R=30 certificate; "
                "this is three finite cases, not an arbitrary-N proof"
                if earliest_saturation else
                "N=2 bridge is not yet certified"
            ),
        },
        {
            "id": "V7-NSOBS-ALL-N-AFTER-N123",
            "name": "arbitrary-finite-N shell-energy earliest-order saturation",
            "tier": "Open",
            "status": "OPEN",
            "evidence": "N=1,2,3 evidence plus all-N structural ceilings and triad connectivity do not by themselves prove independent observable minors for arbitrary finite N",
        },
    ]

    summary = {
        "N": 2,
        "mode_count": k2.nm,
        "real_state_dimension": k2.d,
        "shell_count": ns,
        "shells": k2.shells,
        "translation_ceiling": ceiling,
        "earliest_possible_shell_order": earliest,
        "final_rank_R30": final_rank,
        "milestones": milestones,
        "state_series_sec": state_sec,
        "tangent_sec": time.time() - t1,
        "prime": P,
        "viscosity": "1/200",
        "simulation": False,
        "finite_first_scope": "one fixed finite N=2 Fourier-Galerkin polynomial system; no completed-infinity premise",
    }
    print("RESULT_JSON:" + json.dumps({"claims": claims, "summary": summary}, separators=(",", ":")), flush=True)
    return 0 if all(c["status"] != "FAIL" for c in claims) else 1


if __name__ == "__main__":
    raise SystemExit(main())
