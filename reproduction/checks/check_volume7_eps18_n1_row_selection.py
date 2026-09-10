#!/usr/bin/env python3
"""Deterministic row-chart search for a tighter full N=1 local inverse certificate.

At shell Taylor order zero all three shell-energy rows are structurally available.  At
each later order the energy-balance relation leaves only two new independent shell
rows, so the minimal N=1 chart uses 3 + 2*23 = 49 observations.  The earlier witness
selected the first modularly independent rows; it was never optimized for conditioning.

This checker searches only among the three possible shell-row pairs at each order
1..23.  Floating linear algebra is used *only as a deterministic heuristic* to choose
a candidate chart.  The final chart is then reconstructed and inverted with exact
integer/Fraction arithmetic, and its radius is certified with the already-reproduced
componentwise Hessian-row majorants.

A useful normalization makes the search objective natural.  If H_j>0 is the certified
row-variation bound and M has rows J_j/H_j, then

    J = D_H M,
    J^{-1} D_H = M^{-1},

so the exact defect slope max_i sum_j |(J^{-1})_ij| H_j equals ||M^{-1}||_infinity.
The heuristic therefore minimizes a floating approximation of the same quantity later
certified exactly.

This remains a fixed finite N=1 local result.  It is not a global inverse, not a
measurement-ready tolerance, not an arbitrary-N result, and has no continuum/Clay
implication.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(100_000)

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_componentwise_radius as comp
import check_volume7_eps18_n1_exact_preconditioner as exact
import check_volume7_eps18_n1_small_witness as small

CENTER_SEED = 20260910
BOX_MARGIN = Fraction(1, 1000)
RMAX = 23
PAIRS = ((0, 1), (0, 2), (1, 2))


def selection_from_pairs(pairs_by_order: list[tuple[int, ...]], shell_count: int) -> list[int]:
    rows: list[int] = []
    for order, shells in enumerate(pairs_by_order):
        rows.extend(order * shell_count + s for s in shells)
    return rows


def float_objective(selection, exact_blocks, y2, free, shell_count) -> float:
    rows = []
    for r in selection:
        order, shell = divmod(r, shell_count)
        h = y2[order][shell]
        if h <= 0:
            return math.inf
        rows.append([
            float(Fraction(int(exact_blocks[order][shell, j]), 1) / h)
            for j in free
        ])
    M = np.asarray(rows, dtype=float)
    if M.shape != (49, 49) or not np.all(np.isfinite(M)):
        return math.inf
    try:
        inv = np.linalg.inv(M)
    except np.linalg.LinAlgError:
        return math.inf
    value = float(np.linalg.norm(inv, ord=np.inf))
    return value if math.isfinite(value) else math.inf


def hill_climb(start_pairs, exact_blocks, y2, free, shell_count):
    current = list(start_pairs)
    current_obj = float_objective(
        selection_from_pairs(current, shell_count), exact_blocks, y2, free, shell_count
    )
    swaps = 0
    for _ in range(5):
        changed = False
        for order in range(1, RMAX + 1):
            best_pair = current[order]
            best_obj = current_obj
            for pair in PAIRS:
                trial = list(current)
                trial[order] = pair
                obj = float_objective(
                    selection_from_pairs(trial, shell_count), exact_blocks, y2, free, shell_count
                )
                if obj < best_obj * (1.0 - 1e-12):
                    best_obj = obj
                    best_pair = pair
            if best_pair != current[order]:
                current[order] = best_pair
                current_obj = best_obj
                swaps += 1
                changed = True
        if not changed:
            break
    return current, current_obj, swaps


def exact_radius(selection, exact_blocks, y2, free, shell_count):
    J0 = [
        [int(exact_blocks[r // shell_count][r % shell_count, j]) for j in free]
        for r in selection
    ]
    A, det_j0 = exact.exact_inverse(J0)
    H = [y2[r // shell_count][r % shell_count] for r in selection]
    slopes = [
        sum((abs(A[i][j]) * H[j] for j in range(49)), Fraction(0))
        for i in range(49)
    ]
    slope = max(slopes)
    radius = Fraction(1, 2) / slope
    return radius, slope, det_j0


def main() -> int:
    cube = base.CubeGalerkinModP()
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"]:
        raise RuntimeError("declared small-integer center did not reproduce")

    x0 = small.small_state(CENTER_SEED, cube.d)
    gauge = [int(i) for i in center["gauge_coordinates"]]
    free = [j for j in range(cube.d) if j not in gauge]
    shell_count = len(cube.shells)
    current_selection = [int(r) for r in center["selected_observation_rows"]]

    exact_blocks = exact.exact_scaled_shell_blocks(cube, x0)
    T = comp.scaled_bilinear_tensor(cube)
    sparse_T = comp.sparse_absolute_tensor(T)
    y2 = comp.componentwise_majorants(
        cube, sparse_T, [abs(int(v)) for v in x0], BOX_MARGIN
    )

    # Recover the current structurally minimal pair pattern.
    current_pairs: list[tuple[int, ...]] = []
    for order in range(RMAX + 1):
        shells = tuple(
            r % shell_count
            for r in current_selection
            if r // shell_count == order
        )
        current_pairs.append(shells)
    structure_ok = (
        current_pairs[0] == (0, 1, 2)
        and all(len(current_pairs[n]) == 2 for n in range(1, RMAX + 1))
    )
    if not structure_ok:
        raise RuntimeError(f"unexpected current N=1 row structure: {current_pairs}")

    starts = [current_pairs]
    for pair in PAIRS:
        starts.append([(0, 1, 2)] + [pair for _ in range(RMAX)])
    starts.append([(0, 1, 2)] + [PAIRS[n % 3] for n in range(RMAX)])
    starts.append([(0, 1, 2)] + [PAIRS[(2 * n + 1) % 3] for n in range(RMAX)])

    best_pairs = None
    best_obj = math.inf
    best_swaps = 0
    start_records = []
    for idx, start in enumerate(starts):
        pairs, obj, swaps = hill_climb(start, exact_blocks, y2, free, shell_count)
        start_records.append({"start": idx, "float_objective": obj, "swaps": swaps})
        if obj < best_obj:
            best_obj = obj
            best_pairs = pairs
            best_swaps = swaps

    if best_pairs is None or not math.isfinite(best_obj):
        raise RuntimeError("deterministic row-chart search found no finite candidate")

    best_selection = selection_from_pairs(best_pairs, shell_count)
    current_radius, current_slope, _ = exact_radius(
        current_selection, exact_blocks, y2, free, shell_count
    )
    best_radius, best_slope, best_det = exact_radius(
        best_selection, exact_blocks, y2, free, shell_count
    )

    current_digit, current_bracket = exact.reciprocal_power10_bracket(current_radius)
    best_digit, best_bracket = exact.reciprocal_power10_bracket(best_radius)
    improvement = best_radius / current_radius
    improved = best_radius > current_radius
    box_contained = best_radius <= BOX_MARGIN

    exact_modular_rank = base.rank_mod(
        np.asarray(
            [
                [int(exact_blocks[r // shell_count][r % shell_count, j]) % base.P for j in free]
                for r in best_selection
            ],
            dtype=np.int64,
        )
    )
    exact_ok = best_det != 0 and exact_modular_rank == 49 and box_contained

    claims = [
        {
            "id": "V7-EPSC18-N1-ROW-CHART-SEARCH",
            "name": "deterministic conditioning search over structurally admissible N=1 shell-row pairs",
            "tier": "finite_diagnostic",
            "status": "PASS" if exact_ok else "FAIL",
            "evidence": (
                f"six deterministic starts; best floating objective={best_obj:.6e}; "
                f"final hill-climb swaps={best_swaps}; final chart exact modular rank={exact_modular_rank}"
            ),
        },
        {
            "id": "V7-EPSC18-N1-ROW-OPTIMIZED-RADIUS",
            "name": "exactly certified componentwise radius on the selected N=1 observation chart",
            "tier": "Dr",
            "status": "DERIVED" if exact_ok else "OPEN",
            "evidence": (
                f"final candidate is re-inverted over Q with nonzero exact determinant; {best_bracket}; q<=1/2; "
                f"baseline first-independent chart was {current_bracket}"
                if exact_ok else
                "final candidate did not satisfy exact invertibility/box obligations"
            ),
        },
        {
            "id": "V7-EPSC18-N1-ROW-OPTIMIZATION-GAIN",
            "name": "row-chart optimization improves the certified N=1 componentwise radius",
            "tier": "finite_diagnostic",
            "status": "PASS" if exact_ok and improved else "FAIL",
            "evidence": (
                f"exact radius ratio best/current > 1={improved}; power-of-ten lower-bracket index "
                f"moves from {current_digit} to {best_digit}"
            ),
        },
        {
            "id": "V7-EPSC18-N1-MEASUREMENT-READY-AFTER-ROW-SEARCH",
            "name": "measurement-ready robust inverse after finite observation-row optimization",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "the finite chart is optimized and then exactly recertified, but practical measurement readiness "
                "still requires branch/noise containment and a sufficiently large physically interpreted radius"
            ),
        },
    ]

    summary = {
        "cutoff": 1,
        "slice_dimension": 49,
        "candidate_rows": 72,
        "selected_rows": 49,
        "structural_pattern": "3 rows at order 0; 2 of 3 shell rows at each order 1..23",
        "search_starts": start_records,
        "best_pairs_by_order": [list(p) for p in best_pairs],
        "best_float_objective": best_obj,
        "current_radius_bracket": current_bracket,
        "best_radius_bracket": best_bracket,
        "best_over_current_ratio_float": float(improvement),
        "exact_final_det_nonzero": best_det != 0,
        "exact_final_modular_rank": exact_modular_rank,
        "box_containment_certified": box_contained,
        "q_bound_at_chosen_radius": "1/2",
        "finite_first_scope": (
            "floating search only proposes a finite row chart; final invertibility and radius are certified with exact integers/Fractions"
        ),
    }

    print("EPSC-18 N=1 observation-row chart search and exact recertification")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 0 if all(c["status"] != "FAIL" for c in claims) else 1


if __name__ == "__main__":
    raise SystemExit(main())
