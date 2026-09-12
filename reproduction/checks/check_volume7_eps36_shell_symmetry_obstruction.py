#!/usr/bin/env python3
"""Finite obstruction to global shell-energy branch capture modulo translations alone.

The fixed-N shell-energy reader is invariant under cubic lattice symmetries in addition
to spatial translations.  This checker gives an explicit N=1 witness using the axis
swap Q(x,y,z)=(y,x,z).

Take one divergence-free Fourier mode at k_a=(1,0,0), then apply Q.  In the coordinate
basis used by the existing finite Galerkin checker this gives a one-mode state at
k_b=(0,1,0).  The two states:

* have different Fourier support, so no spatial translation can map one to the other;
* have equal shell energy;
* have zero quadratic self-interaction in the N=1 Galerkin system; and
* have the same viscous rate because |k_a|^2=|k_b|^2=1.

Hence, for every particular finite derivative order n,

    I^(n)(0) = (-2 nu)^n I(0)

for both states.  The equality is a finite induction schema, not an appeal to a
completed infinite sequence.  Therefore shell-energy-only observations cannot provide
global unique branch capture on the translation quotient.  A correct measurement
interface must either quotient the additional cubic symmetry, add an orientation-
breaking reader, or supply an independent admissible-domain/orientation prior.
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

P = base.P
KA = (1, 0, 0)
KB = (0, 1, 0)
FINITE_ORDERS_CHECKED = 32


def shell_value(cube: base.CubeGalerkinModP, x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.int64) % P
    return ((x * x) @ cube.weights.T) % P


def one_mode_state(cube: base.CubeGalerkinModP, k, coeff: int) -> np.ndarray:
    x = np.zeros(cube.d, dtype=np.int64)
    ri = cube.rep_index[k]
    x[4 * ri] = coeff % P
    return x


def support_reps(cube: base.CubeGalerkinModP, x: np.ndarray):
    out = []
    for ri, k in enumerate(cube.reps):
        if any(int(x[4 * ri + j]) % P for j in range(4)):
            out.append(k)
    return out


def main() -> int:
    cube = base.CubeGalerkinModP()
    if cube.d != 52:
        raise RuntimeError("checker is scoped to the declared N=1 cube")

    # For k=(1,0,0), the first basis vector is +z.  Under x<->y it remains +z,
    # while the first basis vector at (0,1,0) is -z, hence coefficient -1.
    xa = one_mode_state(cube, KA, 1)
    xb = one_mode_state(cube, KB, -1)

    e1a = np.asarray(cube.bases[cube.rep_index[KA]][0], dtype=int)
    e1b = np.asarray(cube.bases[cube.rep_index[KB]][0], dtype=int)
    Q = np.asarray(((0, 1, 0), (1, 0, 0), (0, 0, 1)), dtype=int)
    axis_swap_basis_ok = bool(np.array_equal(Q @ e1a, -e1b))

    support_a = support_reps(cube, xa)
    support_b = support_reps(cube, xb)
    support_distinct = support_a == [KA] and support_b == [KB] and KA != KB

    energy_a = shell_value(cube, xa)
    energy_b = shell_value(cube, xb)
    shell_equal = bool(np.array_equal(energy_a % P, energy_b % P))

    nonlinear_a = cube.bilinear(xa, xa) % P
    nonlinear_b = cube.bilinear(xb, xb) % P
    nonlinear_zero = bool(np.all(nonlinear_a == 0) and np.all(nonlinear_b == 0))

    ia = cube.rep_index[KA]
    ib = cube.rep_index[KB]
    lambda_a = int(cube.lin_diag[4 * ia]) % P
    lambda_b = int(cube.lin_diag[4 * ib]) % P
    same_linear_rate = lambda_a == lambda_b

    # For the pure one-mode states F(x)=lambda*x, so the quadratic shell output
    # obeys d^n I/dt^n=(2 lambda)^n I.  Check an arbitrary declared finite prefix;
    # the formula itself is proved by finite induction and does not require a
    # completed sequence object.
    finite_derivatives_equal = True
    derivative_records = []
    for n in range(FINITE_ORDERS_CHECKED + 1):
        fa = pow((2 * lambda_a) % P, n, P)
        fb = pow((2 * lambda_b) % P, n, P)
        ya = (fa * energy_a) % P
        yb = (fb * energy_b) % P
        eq = bool(np.array_equal(ya, yb))
        finite_derivatives_equal = finite_derivatives_equal and eq
        if n in (0, 1, 2, 8, 16, 32):
            derivative_records.append({"order": n, "equal": eq, "shell_vector": [int(v) for v in ya]})

    # A spatial translation multiplies each Fourier coefficient by a phase but does
    # not change its wavevector support.  Since the supports are different, these
    # states are not translation-equivalent.
    not_translation_equivalent = support_distinct

    obstruction = bool(
        axis_swap_basis_ok
        and support_distinct
        and shell_equal
        and nonlinear_zero
        and same_linear_rate
        and finite_derivatives_equal
        and not_translation_equivalent
    )

    claims = [
        {
            "id": "V7-NSOBS-CUBIC-SHELL-SYMMETRY-WITNESS",
            "name": "N=1 shell-energy reader has a non-translation cubic-symmetry alias",
            "tier": "finite_diagnostic",
            "status": "PASS" if obstruction else "FAIL",
            "evidence": (
                f"axis swap sends k={KA} to {KB}; supports differ; shell vectors agree; "
                f"B(x,x)=0 for both; viscous rates agree; derivatives checked through finite order {FINITE_ORDERS_CHECKED}"
            ),
        },
        {
            "id": "V7-EPSC36-GLOBAL-SHELL-BRANCH-CAPTURE-OBSTRUCTION",
            "name": "shell-energy-only data cannot globally select a unique translation-quotient branch",
            "tier": "Dr",
            "status": "DERIVED" if obstruction else "OPEN",
            "evidence": (
                "explicit states with different Fourier support are not translation-equivalent but have identical shell-energy derivative records at every arbitrary finite order by the one-mode finite induction formula"
                if obstruction
                else "explicit symmetry witness did not reproduce"
            ),
        },
        {
            "id": "V7-EPSC36-QUOTIENT-OR-ORIENTATION-REPAIR",
            "name": "repair global branch capture by larger symmetry quotient, orientation-breaking reader, or independent prior",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "the obstruction rules out unique global branch selection modulo translations alone; the next measurement theorem must declare which finite repair is used"
            ),
        },
    ]

    summary = {
        "cutoff": 1,
        "axis_swap": [[int(v) for v in row] for row in Q],
        "state_a_support": [list(k) for k in support_a],
        "state_b_support": [list(k) for k in support_b],
        "shell_energy_a_mod_p": [int(v) for v in energy_a],
        "shell_energy_b_mod_p": [int(v) for v in energy_b],
        "nonlinear_self_interaction_zero": nonlinear_zero,
        "same_linear_rate_mod_p": same_linear_rate,
        "finite_derivative_prefix": derivative_records,
        "translation_support_invariant": True,
        "global_translation_quotient_branch_capture_possible": False if obstruction else None,
        "finite_first_scope": "explicit finite N=1 records plus an arbitrary-finite-order induction formula; no completed N=infinity object",
    }

    print("EPSC-36 shell symmetry branch-capture obstruction")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims, "summary": summary}, separators=(",", ":")))
    return 0 if obstruction else 1


if __name__ == "__main__":
    raise SystemExit(main())
