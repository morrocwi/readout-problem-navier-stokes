#!/usr/bin/env python3
"""Finite N=1 orientation-reader witness for the EPSC-42 symmetry repair.

Shell energy is invariant under the cubic signed-permutation group.  This checker asks a
narrower finite question: can a small additional translation-invariant reader break that
discrete orientation ambiguity at the existing small-integer N=1 center?

Use two finite quadratic/cubic-orientation summaries of the finite Fourier record:

    M_ij = sum_k k_i k_j |u_k|^2
    H    = sum_k u_k^* . (i k x u_k)

where M is the labelled spectral second-moment tensor and H is helicity.  Under a signed
permutation Q in O(3,Z), finite Fourier relabelling gives

    M -> Q M Q^T,
    H -> det(Q) H.

Both are invariant under spatial translations because translations change Fourier
phases only.  For a generic M the only unavoidable signed-permutation stabilizer can be
{+I,-I}; a nonzero pseudoscalar H then removes -I.  The checker enumerates all 48 signed
permutation matrices at the declared N=1 integer center and verifies that the pair (M,H)
has trivial cubic stabilizer.

This is a structural orientation-repair witness, not a proof that the augmented reader
is globally injective on the full state space and not a practical sensor design.
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_volume6_ns_observability as base
import check_volume7_eps18_n1_small_witness as small

P = base.P
CENTER_SEED = 20260910


def det3(Q: np.ndarray) -> int:
    a = [[int(Q[i, j]) for j in range(3)] for i in range(3)]
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def signed_permutations():
    mats = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((-1, 1), repeat=3):
            Q = np.zeros((3, 3), dtype=int)
            for i in range(3):
                Q[i, perm[i]] = signs[i]
            d = det3(Q)
            if d not in (-1, 1):
                raise RuntimeError("signed permutation must be orthogonal")
            mats.append((Q, d))
    if len(mats) != 48:
        raise RuntimeError("expected 48 signed permutation matrices")
    return mats


def spectral_tensor_and_helicity(cube, x):
    U = cube.reconstruct(np.asarray(x, dtype=np.int64) % P)[0]
    M = np.zeros((3, 3), dtype=np.int64)
    H = 0
    for mi, k in enumerate(cube.modes):
        kv = np.asarray(k, dtype=np.int64)
        a = U[mi, :, 0].astype(np.int64) % P
        b = U[mi, :, 1].astype(np.int64) % P
        energy = int(np.sum((a * a + b * b) % P) % P)
        for i in range(3):
            for j in range(3):
                M[i, j] = (M[i, j] + int(kv[i]) * int(kv[j]) * energy) % P

        # Re[u^* . (i k x u)] = 2 k . (a x b).
        cross = np.cross(a, b) % P
        H = (H + 2 * int(np.sum((kv % P) * cross) % P)) % P
    return M % P, int(H % P)


def conjugate_tensor(Q, M):
    return (Q.astype(object) @ M.astype(object) @ Q.T.astype(object)).astype(object)


def matrix_equal_mod(A, B):
    A = np.asarray(A, dtype=object)
    B = np.asarray(B, dtype=object)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if (int(A[i, j]) - int(B[i, j])) % P:
                return False
    return True


def main() -> int:
    cube = base.CubeGalerkinModP()
    x = small.small_state(CENTER_SEED, cube.d)
    center = small.evaluate_candidate(cube, CENTER_SEED)
    if not center["pass"]:
        raise RuntimeError("declared small-integer N=1 center did not reproduce")

    M, helicity = spectral_tensor_and_helicity(cube, x)
    identity = np.eye(3, dtype=int)
    minus_identity = -identity

    tensor_stabilizer = []
    pair_stabilizer = []
    for Q, detq in signed_permutations():
        tensor_same = matrix_equal_mod(conjugate_tensor(Q, M), M)
        if tensor_same:
            tensor_stabilizer.append(Q.tolist())
        hq = (detq * helicity) % P
        if tensor_same and hq == helicity % P:
            pair_stabilizer.append(Q.tolist())

    expected_tensor_stabilizer = [identity.tolist(), minus_identity.tolist()]
    # Compare as sets of flattened integer tuples; enumeration order is irrelevant.
    flat = lambda Q: tuple(v for row in Q for v in row)
    tensor_stab_ok = {flat(Q) for Q in tensor_stabilizer} == {
        flat(Q) for Q in expected_tensor_stabilizer
    }
    pair_stab_ok = {flat(Q) for Q in pair_stabilizer} == {flat(identity.tolist())}
    helicity_nonzero = helicity % P != 0
    pass_all = bool(tensor_stab_ok and helicity_nonzero and pair_stab_ok)

    claims = [
        {
            "id": "V7-EPSC42-N1-SPECTRAL-TENSOR-STABILIZER",
            "name": "labelled spectral second moment reduces the N=1 cubic stabilizer to central inversion at the declared center",
            "tier": "finite_diagnostic",
            "status": "PASS" if tensor_stab_ok else "FAIL",
            "evidence": f"enumerated all 48 signed permutations; tensor stabilizer size={len(tensor_stabilizer)}",
        },
        {
            "id": "V7-EPSC42-N1-ORIENTATION-PAIR-TRIVIAL-STABILIZER",
            "name": "spectral tensor plus nonzero helicity has trivial cubic stabilizer at the declared N=1 center",
            "tier": "finite_diagnostic",
            "status": "PASS" if pass_all else "FAIL",
            "evidence": (
                f"helicity mod {P}={helicity}; pair stabilizer size={len(pair_stabilizer)} after exhaustive 48-element check"
            ),
        },
        {
            "id": "V7-EPSC42-ORIENTATION-READER-GENERIC-CANDIDATE",
            "name": "translation-invariant orientation reader (M,H) is a finite candidate for removing cubic aliases generically",
            "tier": "Dr",
            "status": "DERIVED" if pass_all else "OPEN",
            "evidence": (
                "for each nonidentity signed permutation the equality (Q M Q^T,det(Q)H)=(M,H) is polynomial; one witness breaking all 47 nonidentity elements shows their fixed sets are proper, so outside their finite union the cubic stabilizer is trivial"
                if pass_all else "trivial-stabilizer witness did not reproduce"
            ),
        },
        {
            "id": "V7-EPSC42-AUGMENTED-GLOBAL-INJECTIVITY",
            "name": "global state injectivity of shell samples augmented by (M,H)",
            "tier": "Open",
            "status": "OPEN",
            "evidence": "breaking the declared cubic symmetry does not exclude unrelated global aliases; a global injectivity/exclusion certificate remains separate",
        },
    ]

    summary = {
        "cutoff": 1,
        "center_seed": CENTER_SEED,
        "signed_permutation_count": 48,
        "spectral_tensor_mod_p": [[int(v) for v in row] for row in M],
        "helicity_mod_p": helicity,
        "tensor_stabilizer_size": len(tensor_stabilizer),
        "pair_stabilizer_size": len(pair_stabilizer),
        "translation_invariance": "M and H depend on phase-cancelling Fourier bilinears, so spatial translation phases cancel",
        "what_closed": "explicit finite cubic-orientation ambiguity is removable at the N=1 center by the augmented reader (M,H)" if pass_all else "not closed",
        "what_remains_open": "global injectivity beyond cubic symmetry, practical sensing, arbitrary finite N",
        "finite_first_scope": "52-coordinate finite state, 48 finite group elements, finite Fourier sums; no completed infinity",
    }
    print("EPSC-42 finite orientation-reader symmetry repair")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"claims": claims, "summary": summary}, separators=(",", ":")))
    return 0 if pass_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
