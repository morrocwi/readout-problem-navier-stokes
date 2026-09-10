#!/usr/bin/env python3
"""Search deterministic small-integer N=2 shell-observability inverse centers.

The existing explicit N=2 quotient-chart certificate uses a state sampled across
F_251.  That is enough for local inverse existence, but it is a poor center for a
future characteristic-zero interval/preconditioner certificate.  This checker asks
whether the same 245-dimensional shell chart can already be realized at a center
with coordinates in {-3,-2,-1,1,2,3}.

For each deterministic candidate it:
  * fixes the same explicit three-coordinate translation gauge;
  * propagates the exact F_251 N=2 state and the 245 coordinate tangent directions;
  * stacks shell-energy Taylor rows through R=30;
  * selects 245 independent rows and verifies a nonzero square minor.

A PASS gives a compact integer lift suitable for the next EPSC-18
characteristic-zero preconditioner/interval stage.  It is still only a fixed finite
N=2 statement: no q_2<1 radius, noisy branch capture, arbitrary-N theorem,
continuum regularity, DNS adequacy, or Clay implication is claimed here.
"""
from __future__ import annotations

import json
import time

import numpy as np

import check_k2_energy_observability as k2
import check_k2_shell_explicit_quotient_chart as chart

P = k2.P
RMAX = 30
SLICE_DIM = k2.d - 3
CANDIDATE_SEEDS = (20260910, 1701, 918273, 271828, 314159)
SMALL_VALUES = np.asarray([-3, -2, -1, 1, 2, 3], dtype=np.int64)


def small_state(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.choice(SMALL_VALUES, size=k2.d, replace=True).astype(np.int64)


def evaluate_candidate(seed: int) -> dict:
    ns = len(k2.shells)
    x_signed = small_state(seed)
    x0 = (x_signed % P).astype(np.uint16)

    gauge = chart.axial_gauge_coordinates()
    free = [j for j in range(k2.d) if j not in gauge]
    if len(free) != SLICE_DIM:
        raise RuntimeError("unexpected N=2 slice dimension")

    G = chart.translation_gauge_matrix(x0, gauge)
    gauge_det = chart.det_mod(G)
    if gauge_det == 0:
        return {
            "seed": seed,
            "max_abs_coordinate": int(np.max(np.abs(x_signed))),
            "gauge_coordinates": gauge,
            "gauge_det_mod_p": 0,
            "slice_rank_mod_p": -1,
            "selected_row_count": 0,
            "selected_minor_det_mod_p": 0,
            "max_selected_order": None,
            "pass": False,
        }

    xcoef = np.zeros((RMAX + 1, k2.d), dtype=np.uint16)
    Ux = np.zeros((RMAX + 1, k2.nm, 3, 2), dtype=np.uint16)
    xcoef[0] = x0
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

    Vcoef = np.zeros((RMAX + 1, SLICE_DIM, k2.d), dtype=np.uint16)
    UV = np.zeros((RMAX + 1, SLICE_DIM, k2.nm, 3, 2), dtype=np.uint16)
    for col, coord in enumerate(free):
        Vcoef[0, col, coord] = 1
    k2.recon_batch(Vcoef[0], UV[0], k2.full_rep, k2.full_sign, k2.E1u, k2.E2u, P)
    _ = k2.tangent_rhs(
        0, Vcoef, UV, Ux, k2.linu, k2.starts, k2.tp, k2.tq, k2.modes_arr,
        k2.reps_arr, k2.E1u, k2.E2u, k2.invn1u, k2.invn2u, k2.invk2u, P,
    )

    weights = k2.weights.astype(np.uint16)
    blocks = [chart.shell_block(0, Vcoef, xcoef, weights, P)]
    t1 = time.time()
    for n in range(RMAX):
        rhs = k2.tangent_rhs(
            n, Vcoef, UV, Ux, k2.linu, k2.starts, k2.tp, k2.tq, k2.modes_arr,
            k2.reps_arr, k2.E1u, k2.E2u, k2.invn1u, k2.invn2u, k2.invk2u, P,
        )
        Vcoef[n + 1] = (rhs.astype(np.int64) * pow(n + 1, -1, P) % P).astype(np.uint16)
        k2.recon_batch(Vcoef[n + 1], UV[n + 1], k2.full_rep, k2.full_sign, k2.E1u, k2.E2u, P)
        blocks.append(chart.shell_block(n + 1, Vcoef, xcoef, weights, P))

    Aall = np.vstack(blocks).astype(np.int64) % P
    slice_rank = k2.rank_mod(Aall)
    selected = chart.select_independent_rows(Aall, SLICE_DIM) if slice_rank == SLICE_DIM else []
    det_square = chart.det_mod(Aall[selected, :]) if len(selected) == SLICE_DIM else 0
    passed = bool(slice_rank == SLICE_DIM and len(selected) == SLICE_DIM and det_square != 0)
    selected_orders = [int(r // ns) for r in selected]

    return {
        "seed": seed,
        "max_abs_coordinate": int(np.max(np.abs(x_signed))),
        "state_signed": [int(v) for v in x_signed],
        "gauge_coordinates": [int(v) for v in gauge],
        "gauge_det_mod_p": int(gauge_det),
        "slice_rank_mod_p": int(slice_rank),
        "selected_observation_rows": [int(v) for v in selected],
        "selected_row_count": len(selected),
        "selected_minor_det_mod_p": int(det_square),
        "max_selected_order": max(selected_orders) if selected_orders else None,
        "state_series_sec": state_sec,
        "tangent_and_chart_sec": time.time() - t1,
        "pass": passed,
    }


def main() -> int:
    assert k2.N == 2 and k2.d == 248 and SLICE_DIM == 245 and P == 251 and P > RMAX
    tested = []
    winner = None
    for seed in CANDIDATE_SEEDS:
        rec = evaluate_candidate(seed)
        tested.append({k: v for k, v in rec.items() if k not in ("state_signed", "selected_observation_rows")})
        if rec["pass"]:
            winner = rec
            break

    claims = []
    if winner is None:
        claims.append({
            "id": "V7-EPSC32-N2-SMALL-INTEGER-CENTER",
            "name": "small-integer full-rank center for the explicit N=2 shell quotient chart",
            "tier": "finite_diagnostic",
            "status": "FAIL",
            "evidence": f"no full-rank witness among deterministic candidates {tested}",
        })
    else:
        claims.append({
            "id": "V7-EPSC32-N2-SMALL-INTEGER-CENTER",
            "name": "small-integer full-rank center for the explicit N=2 shell quotient chart",
            "tier": "finite_diagnostic",
            "status": "PASS",
            "evidence": (
                f"seed={winner['seed']}; max|x_j|={winner['max_abs_coordinate']}; "
                f"slice rank={winner['slice_rank_mod_p']}; selected rows={winner['selected_row_count']}; "
                f"minor det mod {P}={winner['selected_minor_det_mod_p']}"
            ),
        })
        claims.append({
            "id": "V7-EPSC32-N2-SMALL-CENTER-CHAR0-INPUT",
            "name": "compact integer lift is available for the N=2 characteristic-zero preconditioner stage",
            "tier": "Dr",
            "status": "DERIVED",
            "evidence": (
                "the same explicit translation slice and 245-row chart have a nonzero good-prime minor at a "
                "state with all coordinates in {-3,-2,-1,1,2,3}; this supplies a deterministic small integer center "
                "for exact characteristic-zero reconstruction"
            ),
        })

    claims.append({
        "id": "V7-EPSC32-N2-QUANTITATIVE-Q2-AFTER-SMALL-CENTER",
        "name": "branch-wide quantitative N=2 inverse certificate q_2<1 around the small center",
        "tier": "Open",
        "status": "OPEN",
        "evidence": "the next stage must reconstruct the selected Jacobian in characteristic zero and certify an inverse/preconditioned Jacobian enclosure on a nonzero real box",
    })

    summary = {
        "N": 2,
        "state_dimension": k2.d,
        "slice_dimension": SLICE_DIM,
        "shell_count": len(k2.shells),
        "max_taylor_order": RMAX,
        "candidate_seeds": list(CANDIDATE_SEEDS),
        "winner_seed": None if winner is None else winner["seed"],
        "winner_max_abs_coordinate": None if winner is None else winner["max_abs_coordinate"],
        "winner_gauge_coordinates": None if winner is None else winner["gauge_coordinates"],
        "winner_selected_minor_det_mod_p": None if winner is None else winner["selected_minor_det_mod_p"],
        "winner_selected_observation_rows": None if winner is None else winner["selected_observation_rows"],
        "winner_state_signed": None if winner is None else winner["state_signed"],
        "prime": P,
        "finite_first_scope": "fixed N=2 finite polynomial system and explicit finite coordinate slice; no completed-infinity premise",
    }

    print("EPSC-18/32 N=2 small-integer witness search")
    print("tested:", json.dumps(tested, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims, "summary": summary}, separators=(",", ":")), flush=True)
    return 0 if winner is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
