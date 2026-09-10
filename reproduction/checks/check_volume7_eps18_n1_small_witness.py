#!/usr/bin/env python3
"""Search a tiny deterministic list of small-integer N=1 observability witnesses.

Purpose: the existing exact modular witness uses coordinates drawn across F_p, which is
excellent for proving generic rank but poor as a center for real interval conditioning.
This checker asks a narrower finite question: does a full-rank symmetry-sliced shell-
energy Taylor-jet witness already occur at a state with small integer coordinates?

A PASS is useful input for the next EPSC-18 interval/Krawczyk stage. It is not itself a
quantitative radius and does not assume any completed infinite Fourier state.
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

P = base.P
RMAX = 23
CANDIDATE_SEEDS = (20260910, 1701, 918273)


def small_state(seed: int, d: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    # Draw from {-3,-2,-1,1,2,3}; avoid zeros so translation-gauge candidates
    # are not accidentally suppressed by the center choice.
    vals = np.asarray([-3, -2, -1, 1, 2, 3], dtype=np.int64)
    return rng.choice(vals, size=d, replace=True).astype(np.int64)


def formal_shell_blocks_from_state(cube: base.CubeGalerkinModP, x0_signed: np.ndarray):
    x0 = np.asarray(x0_signed, dtype=np.int64) % P
    xcoef = [x0]
    dxcoef = [np.eye(cube.d, dtype=np.int64)]
    blocks = []

    for n in range(RMAX + 1):
        dy = np.zeros((cube.d, len(cube.shells)), dtype=np.int64)
        for i in range(n + 1):
            j = n - i
            dy = (
                dy
                + cube.Q_batch(dxcoef[i], xcoef[j])
                + cube.Q_batch(dxcoef[j], xcoef[i])
            ) % P
        blocks.append(dy.T.copy())

        if n == RMAX:
            break

        rhs = (xcoef[n] * cube.lin_diag) % P
        drhs = (dxcoef[n] * cube.lin_diag[None, :]) % P
        for i in range(n + 1):
            j = n - i
            rhs = (rhs + cube.bilinear(xcoef[i], xcoef[j])) % P
            drhs = (
                drhs
                + cube.bilinear(dxcoef[i], xcoef[j])
                + cube.bilinear(xcoef[i], dxcoef[j])
            ) % P

        inv = pow(n + 1, -1, P)
        xcoef.append(rhs * inv % P)
        dxcoef.append(drhs * inv % P)

    return blocks


def evaluate_candidate(cube: base.CubeGalerkinModP, seed: int) -> dict:
    x_signed = small_state(seed, cube.d)
    x_mod = x_signed % P
    blocks = formal_shell_blocks_from_state(cube, x_signed)
    J = np.vstack(blocks) % P
    rank = base.rank_mod(J)

    G = local.translation_tangent(cube, x_mod)
    kernel_ok = bool(np.all((J @ G) % P == 0))
    gauge = local.choose_gauge_coordinates(G) if base.rank_mod(G) == 3 else []
    gauge_det = local.det_mod(G[gauge, :]) if len(gauge) == 3 else 0
    free = [j for j in range(cube.d) if j not in gauge]
    slice_rank = base.rank_mod(J[:, free]) if len(free) == 49 else -1
    rows = local.choose_independent_rows(J[:, free], 49) if slice_rank == 49 else []
    minor_det = local.det_mod(J[rows, :][:, free]) if len(rows) == 49 else 0

    return {
        "seed": seed,
        "max_abs_coordinate": int(np.max(np.abs(x_signed))),
        "state_signed": [int(v) for v in x_signed],
        "full_rank": int(rank),
        "translation_kernel_ok": kernel_ok,
        "gauge_coordinates": gauge,
        "gauge_det_mod_p": int(gauge_det),
        "slice_rank": int(slice_rank),
        "selected_observation_rows": rows,
        "minor_det_mod_p": int(minor_det),
        "pass": bool(
            rank == 49
            and kernel_ok
            and len(gauge) == 3
            and gauge_det != 0
            and slice_rank == 49
            and len(rows) == 49
            and minor_det != 0
        ),
    }


def main() -> int:
    cube = base.CubeGalerkinModP()
    tested = []
    winner = None
    for seed in CANDIDATE_SEEDS:
        rec = evaluate_candidate(cube, seed)
        tested.append({k: v for k, v in rec.items() if k != "state_signed"})
        if rec["pass"]:
            winner = rec
            break

    claims = []
    if winner is None:
        claims.append({
            "id": "V7-EPSC18-N1-SMALL-INTEGER-CENTER",
            "name": "small-integer full-rank center for the N=1 symmetry-fixed inverse",
            "tier": "finite_diagnostic",
            "status": "FAIL",
            "evidence": f"no full-rank witness among deterministic candidates {tested}",
        })
    else:
        claims.append({
            "id": "V7-EPSC18-N1-SMALL-INTEGER-CENTER",
            "name": "small-integer full-rank center for the N=1 symmetry-fixed inverse",
            "tier": "finite_diagnostic",
            "status": "PASS",
            "evidence": (
                f"seed={winner['seed']}; max|x_j|={winner['max_abs_coordinate']}; "
                f"rank={winner['full_rank']}; slice_rank={winner['slice_rank']}; "
                f"minor det mod {P}={winner['minor_det_mod_p']}"
            ),
        })

    claims.append({
        "id": "V7-EPSC18-N1-SMALL-CENTER-INTERVAL-RADIUS",
        "name": "useful q<1 interval/Krawczyk radius around the small-integer N=1 center",
        "tier": "Open",
        "status": "OPEN",
        "evidence": (
            "a small exact center reduces avoidable scaling, but a certified interval enclosure "
            "of the selected 49x49 Jacobian over a nonzero box is still required"
        ),
    })

    print("EPSC-18 N=1 small-integer witness search")
    print("tested:", json.dumps(tested, sort_keys=True))
    if winner is not None:
        print("winner_state:", json.dumps(winner["state_signed"]))
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 0 if winner is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
