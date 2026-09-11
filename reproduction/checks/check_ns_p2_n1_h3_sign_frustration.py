#!/usr/bin/env python3
"""Exact N=1 classifier for a naive phase/sign-frustration candidate.

Build the repository's exact integer-scaled 52^3 quadratic Galerkin tensor and the
cubic polynomial for nonlinear production of the inhomogeneous H^3 squared norm,

    Q_3(x) = sum_i W_i x_i (C B(x,x))_i,
    W_i = physical_coordinate_weight_i * (1+|k_i|^2)^3.

After aggregation into commutative cubic monomials, ask whether a real-coordinate
sign assignment x_i in {+1,-1} can make every nonzero monomial contribution have
the same positive sign.  This becomes an exact GF(2) linear system.

SAT means the naive statement 'the exact N=1 H3 production polynomial has an
unavoidable sign-frustration at the coordinate-monomial level' is REFUTED.
UNSAT means an exact algebraic sign-frustration exists at this finite level.

Either outcome is a classification of this precise finite candidate only.  It is
not an all-N theorem and does not by itself prove a quantitative contraction.
"""
from __future__ import annotations

from collections import defaultdict
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_componentwise_radius as componentwise


def physical_weights(cube: base.CubeGalerkinModP) -> list[int]:
    out = []
    for _, _, n1, n2 in cube.bases:
        out.extend([int(n1), int(n1), int(n2), int(n2)])
    return out


def k2_by_coordinate(cube: base.CubeGalerkinModP) -> list[int]:
    out = []
    for k in cube.reps:
        kk = sum(int(v)*int(v) for v in k)
        out.extend([kk]*4)
    return out


def h3_production_coeffs(cube: base.CubeGalerkinModP):
    T = componentwise.scaled_bilinear_tensor(cube)
    pw = physical_weights(cube)
    k2 = k2_by_coordinate(cube)
    W = [pw[i] * (1+k2[i])**3 for i in range(cube.d)]
    coeffs: dict[tuple[int,int,int], int] = defaultdict(int)
    for i in range(cube.d):
        wi = W[i]
        for j in range(cube.d):
            for k in range(cube.d):
                c = int(T[i][j][k])
                if c:
                    coeffs[tuple(sorted((i,j,k)))] += wi*c
    return {m:c for m,c in coeffs.items() if c != 0}, W


def parity_mask(monomial: tuple[int,int,int]) -> int:
    mask = 0
    for idx in monomial:
        mask ^= 1 << idx  # repeated variable contributes even power -> cancels mod 2
    return mask


def solve_xor(rows: list[tuple[int,int,int]]):
    """rows are (mask,rhs,source_id). Return SAT assignment or UNSAT source trace."""
    basis: dict[int, tuple[int,int,int]] = {}
    # trace is a Python int bitset over source equation ids.
    for mask, rhs, sid in rows:
        trace = 1 << sid
        m, b, tr = mask, rhs, trace
        while m:
            p = m.bit_length()-1
            if p not in basis:
                basis[p] = (m,b,tr)
                break
            bm, bb, bt = basis[p]
            m ^= bm
            b ^= bb
            tr ^= bt
        if m == 0 and b:
            sources = [i for i in range(len(rows)) if (tr >> i) & 1]
            return False, None, sources

    # Back-substitution with free variables set to zero.
    assignment = 0
    for p in sorted(basis):
        m,b,_ = basis[p]
        lower = m & ~(1 << p)
        parity = (assignment & lower).bit_count() & 1
        bit = b ^ parity
        if bit:
            assignment |= 1 << p
    return True, assignment, None


def main() -> int:
    cube = base.CubeGalerkinModP()
    if cube.d != 52:
        raise AssertionError(f'expected N=1 dimension 52, got {cube.d}')
    coeffs, W = h3_production_coeffs(cube)
    if not coeffs:
        raise AssertionError('H3 nonlinear production unexpectedly vanished identically')

    items = sorted(coeffs.items())
    rows = []
    for sid,(monomial,coeff) in enumerate(items):
        # Want sign(coeff) * product sign(x_i) = +1.
        # x_i=(-1)^b_i, so parity = 0 for coeff>0 and 1 for coeff<0.
        rows.append((parity_mask(monomial), 0 if coeff > 0 else 1, sid))

    sat, assignment, conflict = solve_xor(rows)

    # Independently verify a SAT assignment if one exists.
    if sat:
        for (monomial, coeff), (mask, rhs, _) in zip(items, rows):
            parity = (assignment & mask).bit_count() & 1
            if parity != rhs:
                raise AssertionError('internal XOR solution verification failed')
        result = 'SAT_ALL_MONOMIAL_SIGNS_ALIGNABLE'
        candidate_status = 'REFUTED'
        conflict_size = 0
    else:
        # Verify the tracked subset XORs to 0=1.
        mm = bb = 0
        for sid in conflict:
            mm ^= rows[sid][0]
            bb ^= rows[sid][1]
        if mm != 0 or bb != 1:
            raise AssertionError('UNSAT trace did not reconstruct 0=1')
        result = 'UNSAT_EXACT_SIGN_FRUSTRATION'
        candidate_status = 'SURVIVES_FINITE_SIGN_TEST'
        conflict_size = len(conflict)

    positive = sum(1 for c in coeffs.values() if c>0)
    negative = sum(1 for c in coeffs.values() if c<0)
    summary = {
        'cutoff': 1,
        'dimension': cube.d,
        'h3_weight_min': min(W),
        'h3_weight_max': max(W),
        'nonzero_aggregated_cubic_monomials': len(coeffs),
        'positive_coefficients': positive,
        'negative_coefficients': negative,
        'xor_rank_upper_bound': min(cube.d, len(rows)),
        'classification': result,
        'naive_unavoidable_sign_frustration_candidate_status': candidate_status,
        'unsat_conflict_equation_count': conflict_size,
        'scope': 'exact N=1 real-coordinate sign level; no all-N or quantitative contraction conclusion',
    }
    print('NS P2 N=1 exact H3 sign-frustration classification')
    print(json.dumps(summary, indent=2, sort_keys=True))
    print('NS-P2 N1 H3 SIGN-FRUSTRATION CLASSIFIER PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
