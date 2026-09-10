#!/usr/bin/env python3
"""Exact finite witness for the full N=1 local observability inverse chart.

This checker stays entirely inside the finite 52-real-dimensional Fourier-Galerkin
model used by the existing N=1 energy-observability checker. It does not assume a
completed infinite Fourier state.

What it certifies:
  * the N=1 shell-energy Taylor jet has exact rank 49 over F_p;
  * the three infinitesimal translation directions lie in that kernel;
  * an explicit 3-coordinate gauge is transverse to translation;
  * after fixing that gauge, an explicit 49x49 observation minor is nonzero mod p.

Because the finite Galerkin map and the chosen witness are rational and p does not
annihilate any declared denominator, a nonzero minor modulo p implies that the
corresponding characteristic-zero rational minor is nonzero. The ordinary finite-
dimensional inverse-function theorem therefore gives a local real inverse on that
symmetry slice.

A later finite checker now also supplies a strictly positive quantitative radius.
That radius is mathematically non-vacuous but still extremely conservative, so this
file distinguishes "positive quantitative radius" from a practically informative
noise/measurement radius. It does NOT claim robust branch capture, global injectivity,
an all-N theorem, a continuum regularity theorem, or a Clay Navier-Stokes result.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

# Import the already-reproduced finite N=1 Galerkin construction instead of
# duplicating the Navier-Stokes algebra.
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base

P = base.P
SEED = 20260909
RMAX = 23


def rank_mod(A: np.ndarray) -> int:
    return base.rank_mod(np.asarray(A, dtype=np.int64) % P)


def det_mod(A: np.ndarray) -> int:
    """Exact determinant modulo P by Gaussian elimination."""
    A = np.asarray(A, dtype=np.int64).copy() % P
    n, m = A.shape
    if n != m:
        raise ValueError("det_mod requires a square matrix")
    det = 1
    for col in range(n):
        pivot = next((r for r in range(col, n) if int(A[r, col]) % P), None)
        if pivot is None:
            return 0
        if pivot != col:
            A[[col, pivot]] = A[[pivot, col]]
            det = (-det) % P
        pv = int(A[col, col]) % P
        det = det * pv % P
        inv = pow(pv, -1, P)
        A[col] = A[col] * inv % P
        for r in range(col + 1, n):
            c = int(A[r, col]) % P
            if c:
                A[r] = (A[r] - c * A[col]) % P
    return int(det % P)


def witness_state(d: int) -> np.ndarray:
    rng = np.random.default_rng(SEED)
    return rng.integers(1, P, size=d, dtype=np.int64)


def translation_tangent(cube: base.CubeGalerkinModP, x0: np.ndarray) -> np.ndarray:
    """Return d x 3 infinitesimal translation matrix in the cube coordinates.

    For z=a+ib at Fourier wavevector k, translation by alpha sends
    z -> exp(i k.alpha) z, hence d/d alpha_j at zero is i k_j z.
    """
    G = np.zeros((cube.d, 3), dtype=np.int64)
    for ri, k in enumerate(cube.reps):
        ar, ai, br, bi = [int(x0[4 * ri + j]) % P for j in range(4)]
        for axis in range(3):
            kj = int(k[axis]) % P
            G[4 * ri + 0, axis] = (-kj * ai) % P
            G[4 * ri + 1, axis] = (kj * ar) % P
            G[4 * ri + 2, axis] = (-kj * bi) % P
            G[4 * ri + 3, axis] = (kj * br) % P
    return G


def choose_independent_rows(A: np.ndarray, target_rank: int) -> list[int]:
    chosen: list[int] = []
    r = 0
    for i in range(A.shape[0]):
        trial = A[chosen + [i], :]
        r2 = rank_mod(trial)
        if r2 > r:
            chosen.append(i)
            r = r2
            if r == target_rank:
                return chosen
    return chosen


def choose_gauge_coordinates(G: np.ndarray) -> list[int]:
    """Choose three coordinate rows whose restriction to translation is invertible."""
    chosen = choose_independent_rows(G, 3)
    if len(chosen) != 3:
        raise RuntimeError("could not find a 3-coordinate translation-transverse gauge")
    return chosen


def row_label(global_row: int, shell_count: int) -> dict:
    order = global_row // shell_count
    shell_slot = global_row % shell_count
    return {"taylor_order": int(order), "shell_slot": int(shell_slot)}


def main() -> int:
    cube = base.CubeGalerkinModP()
    if cube.d != 52 or len(cube.shells) != 3:
        raise RuntimeError("this checker is scoped specifically to the declared N=1 cube")

    # Same exact modular witness used by the existing reproduced rank calculation.
    x0 = witness_state(cube.d)
    blocks = cube.formal_shell_blocks(Rmax=RMAX, seed=SEED)
    J = np.vstack(blocks) % P  # 72 x 52 for orders 0..23 and three shells.

    full_rank = rank_mod(J)
    G = translation_tangent(cube, x0)
    gauge_kernel_defect = np.max(np.abs((J @ G) % P)) if J.size else 0

    gauge_coords = choose_gauge_coordinates(G)
    gauge_matrix = G[gauge_coords, :] % P
    gauge_det = det_mod(gauge_matrix)
    free_cols = [j for j in range(cube.d) if j not in gauge_coords]

    J_slice = J[:, free_cols] % P
    slice_rank = rank_mod(J_slice)
    obs_rows = choose_independent_rows(J_slice, 49)
    if len(obs_rows) == 49:
        minor = J_slice[obs_rows, :]
        minor_det = det_mod(minor)
    else:
        minor_det = 0

    # Denominators used by the finite construction are generated by 200,
    # basis norms, and Taylor divisors 1..24. P=1,000,003 is larger than
    # these and is not divisible by any of them.
    denominator_guard = (
        P > 200
        and math.gcd(P, 200) == 1
        and all(math.gcd(P, n) == 1 for n in range(1, RMAX + 2))
    )

    translation_kernel_ok = full_rank == 49 and gauge_kernel_defect == 0
    gauge_ok = len(gauge_coords) == 3 and gauge_det != 0
    minor_ok = slice_rank == 49 and len(obs_rows) == 49 and minor_det != 0
    characteristic_zero_lift_ok = denominator_guard and minor_ok

    claims = [
        {
            "id": "V7-EPSC18-N1-TRANSLATION-SLICE",
            "name": "explicit three-coordinate gauge is transverse to N=1 spatial translation",
            "tier": "finite_diagnostic",
            "status": "PASS" if translation_kernel_ok and gauge_ok else "FAIL",
            "evidence": (
                f"rank(J)={full_rank}; J*G mod p max={int(gauge_kernel_defect)}; "
                f"gauge_coords={gauge_coords}; det(G_gauge) mod p={gauge_det}"
            ),
        },
        {
            "id": "V7-EPSC18-N1-49X49-MINOR",
            "name": "explicit symmetry-fixed 49x49 shell-energy Taylor-jet minor is nonzero",
            "tier": "finite_diagnostic",
            "status": "PASS" if minor_ok else "FAIL",
            "evidence": (
                f"slice_rank={slice_rank}; selected_rows={len(obs_rows)}; "
                f"det(minor) mod {P}={minor_det}"
            ),
        },
        {
            "id": "V7-EPSC18-N1-LOCAL-INVERSE-EXISTENCE",
            "name": "full N=1 finite quotient has a local real energy-jet inverse on the certified slice",
            "tier": "Dr",
            "status": "DERIVED" if characteristic_zero_lift_ok else "OPEN",
            "evidence": (
                "nonzero rational 49x49 Jacobian minor follows from the nonzero good-prime reduction; "
                "finite-dimensional inverse-function theorem then gives a local real inverse on the slice"
                if characteristic_zero_lift_ok
                else "required nonzero good-prime slice minor was not certified"
            ),
        },
        {
            "id": "V7-EPSC18-N1-QUANTITATIVE-RADIUS",
            "name": "strictly positive certified numerical radius for the full N=1 local inverse",
            "tier": "Dr",
            "status": "DERIVED",
            "evidence": (
                "proved by check_volume7_eps18_n1_explicit_radius.py and tightened by "
                "check_volume7_eps18_n1_rowwise_radius.py; this is a mathematical positive-radius "
                "certificate, not yet a practically informative measurement tolerance"
            ),
        },
        {
            "id": "V7-EPSC18-N1-PRACTICAL-RADIUS",
            "name": "practically informative certified radius for the full N=1 energy-jet inverse",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "requires an effective entrywise interval Jacobian/preconditioner and robust branch/noise handling; "
                "the current rigorous positive radii remain extremely conservative"
            ),
        },
    ]

    result = {
        "prime": P,
        "seed": SEED,
        "cutoff": 1,
        "state_dimension": cube.d,
        "translation_dimension": 3,
        "slice_dimension": len(free_cols),
        "shells": [int(s) for s in cube.shells],
        "max_taylor_order": RMAX,
        "full_jet_rank_mod_p": full_rank,
        "translation_kernel_defect_mod_p": int(gauge_kernel_defect),
        "gauge_coordinates": gauge_coords,
        "gauge_det_mod_p": gauge_det,
        "slice_rank_mod_p": slice_rank,
        "observation_rows": [row_label(i, len(cube.shells)) for i in obs_rows],
        "minor_det_mod_p": minor_det,
        "denominator_guard": denominator_guard,
        "finite_first_scope": (
            "all objects in this witness are finite: 52 coordinates, 3 gauge directions, "
            "72 candidate scalar Taylor observations, and one selected 49x49 minor"
        ),
    }

    failed = [c for c in claims if c["status"] == "FAIL"]
    print("EPSC-18 full N=1 finite local-inverse witness")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims}, separators=(",", ":")))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
