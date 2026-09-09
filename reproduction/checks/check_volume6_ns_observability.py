#!/usr/bin/env python3
"""
Finite Navier--Stokes readout-observability diagnostics.

This script continues the exact NS -> retained-readout lineage without fitting a closure.
It has two deliberately separate parts.

A) Exact small Galerkin subcase (analytic result, finitely checked here)
   A single 2D vorticity triad embedded in 3D periodic NS:
       a=(1,0,0), b=(1,1,0), c=(-2,-1,0), a+b+c=0.
   The shell-energy future is globally closed by four real invariants (x,y,z,r), and
   J0,J1 determine them.  Thus the analytic note proves R*=1 for this subcase.

B) Full 3D cube truncation (exact modular rank witness)
   Retained wavevectors k in {-1,0,1}^3 with the zero mode removed. There are 26 Fourier
   modes and 52 real divergence-free degrees of freedom. We construct the rational
   Fourier-Galerkin NS vector field directly, expand the formal Taylor solution over the
   prime field F_p, propagate the exact tangent series, and compute the rank of the
   shell-readout Taylor coefficients with Gaussian elimination mod p.

A nonzero r x r minor modulo a good prime proves that the corresponding rational
polynomial minor is not identically zero. Combined with the independent 3D spatial-
translation gauge upper bound, the companion note identifies the generic local quotient
dimension. This does NOT prove global ideal stabilization R_M^star.

No continuum regularity, no singularity, no empirical turbulence validation, and no
speed-up claim is made here.
"""
from __future__ import annotations

import itertools
import json
import sys
from fractions import Fraction

import numpy as np

P = 1_000_003
NU = Fraction(1, 200)
NU_MOD = NU.numerator * pow(NU.denominator, -1, P) % P


def triad_exact_check():
    a = (1, 0, 0)
    b = (1, 1, 0)
    c = (-2, -1, 0)

    def k2(k):
        return sum(v * v for v in k)

    def cross2(k, q):
        return k[0] * q[1] - k[1] * q[0]

    ca = Fraction(cross2(b, c), 1) * (Fraction(1, k2(b)) - Fraction(1, k2(c)))
    cb = Fraction(cross2(c, a), 1) * (Fraction(1, k2(c)) - Fraction(1, k2(a)))
    cc = Fraction(cross2(a, b), 1) * (Fraction(1, k2(a)) - Fraction(1, k2(b)))

    expected = (Fraction(3, 10), Fraction(-4, 5), Fraction(1, 2))
    coeff_ok = (ca, cb, cc) == expected
    enstrophy_ok = (ca + cb + cc) == 0
    energy_ok = ca / k2(a) + cb / k2(b) + cc / k2(c) == 0

    x = y = z = Fraction(1, 1)
    r_A = Fraction(1, 1)
    r_B = Fraction(0, 1)
    j1_A = (
        2 * ca * r_A - 2 * NU * k2(a) * x,
        2 * cb * r_A - 2 * NU * k2(b) * y,
        2 * cc * r_A - 2 * NU * k2(c) * z,
    )
    j1_B = (
        2 * ca * r_B - 2 * NU * k2(a) * x,
        2 * cb * r_B - 2 * NU * k2(b) * y,
        2 * cc * r_B - 2 * NU * k2(c) * z,
    )
    r0_insufficient = j1_A != j1_B
    recovered_r = (j1_A[0] + 2 * NU * k2(a) * x) / (2 * ca)
    r_recovery_ok = recovered_r == r_A

    damping_sum = NU * (k2(a) + k2(b) + k2(c))
    reduced_rhs_sample = ca * y * z + cb * x * z + cc * x * y - damping_sum * r_A
    closure_is_rational = isinstance(reduced_rhs_sample, Fraction)

    ok = coeff_ok and enstrophy_ok and energy_ok and r0_insufficient and r_recovery_ok and closure_is_rational
    return ok, {
        "wavevectors": [a, b, c],
        "k2": [k2(a), k2(b), k2(c)],
        "coefficients": [str(ca), str(cb), str(cc)],
        "enstrophy_transfer_sum": str(ca + cb + cc),
        "energy_transfer_sum": str(ca / k2(a) + cb / k2(b) + cc / k2(c)),
        "same_J0_different_J1": r0_insufficient,
        "recovered_r": str(recovered_r),
        "analytic_Rstar": 1,
        "generic_reduced_dimension": 4,
        "full_real_dimension": 6,
    }


class CubeGalerkinModP:
    def __init__(self):
        self.modes = [k for k in itertools.product((-1, 0, 1), repeat=3) if k != (0, 0, 0)]
        self.mode_index = {k: i for i, k in enumerate(self.modes)}
        self.reps = [k for k in self.modes if next(v for v in k if v != 0) > 0]
        self.rep_index = {k: i for i, k in enumerate(self.reps)}
        self.d = 4 * len(self.reps)

        self.bases = [self._basis(k) for k in self.reps]
        self.E1 = np.asarray([b[0] for b in self.bases], dtype=np.int64) % P
        self.E2 = np.asarray([b[1] for b in self.bases], dtype=np.int64) % P
        self.inv_n1 = np.asarray([pow(b[2], -1, P) for b in self.bases], dtype=np.int64)
        self.inv_n2 = np.asarray([pow(b[3], -1, P) for b in self.bases], dtype=np.int64)
        self.k2_rep = np.asarray([sum(v * v for v in k) for k in self.reps], dtype=np.int64)

        self.full_to_rep = []
        for k in self.modes:
            if next(v for v in k if v != 0) > 0:
                rk, conj = k, False
            else:
                rk, conj = tuple(-v for v in k), True
            self.full_to_rep.append((self.rep_index[rk], conj))

        self.triads = [[] for _ in self.modes]
        for ki, k in enumerate(self.modes):
            for pi, pm in enumerate(self.modes):
                q = tuple(k[j] - pm[j] for j in range(3))
                qi = self.mode_index.get(q)
                if qi is not None:
                    self.triads[ki].append((pi, qi))

        self.shells = sorted({sum(v * v for v in k) for k in self.reps})
        shell_index = {q: i for i, q in enumerate(self.shells)}
        self.weights = np.zeros((len(self.shells), self.d), dtype=np.int64)
        for ri, k in enumerate(self.reps):
            si = shell_index[sum(v * v for v in k)]
            n1, n2 = self.bases[ri][2], self.bases[ri][3]
            self.weights[si, 4 * ri] = n1
            self.weights[si, 4 * ri + 1] = n1
            self.weights[si, 4 * ri + 2] = n2
            self.weights[si, 4 * ri + 3] = n2
        self.weights %= P
        self.lin_diag = np.repeat((-NU_MOD * self.k2_rep) % P, 4).astype(np.int64)

    @staticmethod
    def _basis(k):
        kv = np.asarray(k, dtype=int)
        for axis in (np.asarray((1, 0, 0)), np.asarray((0, 1, 0)), np.asarray((0, 0, 1))):
            e1 = np.cross(kv, axis)
            if np.any(e1 != 0):
                break
        e2 = np.cross(kv, e1)
        n1 = int(np.dot(e1, e1))
        n2 = int(np.dot(e2, e2))
        return e1.astype(int), e2.astype(int), n1, n2

    def reconstruct(self, X):
        X = np.asarray(X, dtype=np.int64) % P
        if X.ndim == 1:
            X = X[None, :]
        batch = X.shape[0]
        U = np.zeros((batch, len(self.modes), 3, 2), dtype=np.int64)
        for mi, (ri, conj) in enumerate(self.full_to_rep):
            ar = X[:, 4 * ri]
            ai = X[:, 4 * ri + 1]
            br = X[:, 4 * ri + 2]
            bi = X[:, 4 * ri + 3]
            if conj:
                ai = (-ai) % P
                bi = (-bi) % P
            U[:, mi, :, 0] = (ar[:, None] * self.E1[ri] + br[:, None] * self.E2[ri]) % P
            U[:, mi, :, 1] = (ai[:, None] * self.E1[ri] + bi[:, None] * self.E2[ri]) % P
        return U

    def bilinear(self, A, B):
        A = np.asarray(A, dtype=np.int64) % P
        B = np.asarray(B, dtype=np.int64) % P
        a_was_1d, b_was_1d = A.ndim == 1, B.ndim == 1
        if a_was_1d:
            A = A[None, :]
        if b_was_1d:
            B = B[None, :]
        if A.shape[0] != B.shape[0]:
            if A.shape[0] == 1:
                A = np.broadcast_to(A, (B.shape[0], self.d))
            elif B.shape[0] == 1:
                B = np.broadcast_to(B, (A.shape[0], self.d))
            else:
                raise ValueError("incompatible batch sizes")
        batch = A.shape[0]
        UA, UB = self.reconstruct(A), self.reconstruct(B)
        out = np.zeros((batch, self.d), dtype=np.int64)

        for ri, k in enumerate(self.reps):
            ki = self.mode_index[k]
            vre = np.zeros((batch, 3), dtype=np.int64)
            vim = np.zeros((batch, 3), dtype=np.int64)
            for pi, qi in self.triads[ki]:
                qv = np.asarray(self.modes[qi], dtype=np.int64)
                sr = np.sum(UA[:, pi, :, 0] * qv[None, :], axis=1) % P
                si = np.sum(UA[:, pi, :, 1] * qv[None, :], axis=1) % P
                br = UB[:, qi, :, 0]
                bi = UB[:, qi, :, 1]
                vre = (vre + sr[:, None] * br - si[:, None] * bi) % P
                vim = (vim + sr[:, None] * bi + si[:, None] * br) % P

            qr, qi_im = vim % P, (-vre) % P
            kv = np.asarray(k, dtype=np.int64)
            k2 = sum(v * v for v in k)
            inv_k2 = pow(k2, -1, P)
            dot_r = np.sum(qr * kv[None, :], axis=1) % P
            dot_i = np.sum(qi_im * kv[None, :], axis=1) % P
            pr = (qr - (dot_r[:, None] * kv[None, :] % P) * inv_k2) % P
            pi2 = (qi_im - (dot_i[:, None] * kv[None, :] % P) * inv_k2) % P

            e1, e2 = self.E1[ri], self.E2[ri]
            out[:, 4 * ri] = (np.sum(pr * e1[None, :], axis=1) % P) * self.inv_n1[ri] % P
            out[:, 4 * ri + 1] = (np.sum(pi2 * e1[None, :], axis=1) % P) * self.inv_n1[ri] % P
            out[:, 4 * ri + 2] = (np.sum(pr * e2[None, :], axis=1) % P) * self.inv_n2[ri] % P
            out[:, 4 * ri + 3] = (np.sum(pi2 * e2[None, :], axis=1) % P) * self.inv_n2[ri] % P

        if a_was_1d and b_was_1d:
            return out[0]
        return out

    def Q_batch(self, A, b):
        A = np.asarray(A, dtype=np.int64) % P
        if A.ndim == 1:
            A = A[None, :]
        b = np.asarray(b, dtype=np.int64) % P
        return ((A * b[None, :]) % P) @ self.weights.T % P

    def formal_shell_blocks(self, Rmax=50, seed=20260909):
        rng = np.random.default_rng(seed)
        x0 = rng.integers(1, P, size=self.d, dtype=np.int64)
        xcoef = [x0]
        dxcoef = [np.eye(self.d, dtype=np.int64)]
        blocks = []

        for n in range(Rmax + 1):
            dy = np.zeros((self.d, len(self.shells)), dtype=np.int64)
            for i in range(n + 1):
                j = n - i
                dy = (dy + self.Q_batch(dxcoef[i], xcoef[j]) + self.Q_batch(dxcoef[j], xcoef[i])) % P
            blocks.append(dy.T.copy())

            if n == Rmax:
                break

            rhs = (xcoef[n] * self.lin_diag) % P
            drhs = (dxcoef[n] * self.lin_diag[None, :]) % P
            for i in range(n + 1):
                j = n - i
                rhs = (rhs + self.bilinear(xcoef[i], xcoef[j])) % P
                drhs = (
                    drhs
                    + self.bilinear(dxcoef[i], xcoef[j])
                    + self.bilinear(xcoef[i], dxcoef[j])
                ) % P

            inv = pow(n + 1, -1, P)
            xcoef.append(rhs * inv % P)
            dxcoef.append(drhs * inv % P)

        return blocks


def rank_mod(A):
    A = np.asarray(A, dtype=np.int64).copy() % P
    rows, cols = A.shape
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if A[r, col] % P), None)
        if pivot is None:
            continue
        if pivot != rank:
            A[[rank, pivot]] = A[[pivot, rank]]
        A[rank] = A[rank] * pow(int(A[rank, col]), -1, P) % P
        for r in range(rank + 1, rows):
            if A[r, col]:
                A[r] = (A[r] - A[r, col] * A[rank]) % P
        rank += 1
        if rank == min(rows, cols):
            break
    return rank


def cumulative_ranks(blocks):
    d = blocks[0].shape[1]
    A = np.empty((0, d), dtype=np.int64)
    out = []
    for b in blocks:
        A = np.vstack((A, b))
        out.append(rank_mod(A))
    return out


def cube_rank_check():
    cube = CubeGalerkinModP()
    blocks = cube.formal_shell_blocks(Rmax=50)
    shell_ranks = cumulative_ranks(blocks)
    total_blocks = [np.sum(b, axis=0, keepdims=True) % P for b in blocks]
    total_ranks = cumulative_ranks(total_blocks)

    max_rank_from_translation_gauge = cube.d - 3
    shell_first_max = next((i for i, r in enumerate(shell_ranks) if r == max_rank_from_translation_gauge), None)
    total_first_max = next((i for i, r in enumerate(total_ranks) if r == max_rank_from_translation_gauge), None)

    shell_pattern_ok = all(
        shell_ranks[R] == min(3 + 2 * R, max_rank_from_translation_gauge)
        for R in range(len(shell_ranks))
    )
    total_pattern_ok = all(
        total_ranks[R] == min(1 + R, max_rank_from_translation_gauge)
        for R in range(len(total_ranks))
    )

    ok = (
        cube.d == 52
        and len(cube.shells) == 3
        and max_rank_from_translation_gauge == 49
        and shell_first_max == 23
        and total_first_max == 48
        and shell_pattern_ok
        and total_pattern_ok
    )

    return ok, {
        "prime": P,
        "viscosity": str(NU),
        "mode_count": len(cube.modes),
        "real_state_dimension": cube.d,
        "shells_k2": cube.shells,
        "translation_gauge_dimension": 3,
        "max_generic_local_rank": max_rank_from_translation_gauge,
        "shell_first_rank49_order": shell_first_max,
        "total_energy_first_rank49_order": total_first_max,
        "shell_rank_0_24": shell_ranks[:25],
        "total_rank_0_50": total_ranks,
        "shell_pattern": "rank_R = min(3+2R,49) for R=0..50 in this modular witness",
        "total_pattern": "rank_R = min(1+R,49) for R=0..50 in this modular witness",
        "dimension_ratio_generic_local": max_rank_from_translation_gauge / cube.d,
    }


def main():
    triad_ok, triad = triad_exact_check()
    cube_ok, cube = cube_rank_check()

    print("[exact triad subcase]")
    print("  coefficients:", triad["coefficients"])
    print("  enstrophy transfer sum:", triad["enstrophy_transfer_sum"])
    print("  kinetic-energy transfer sum:", triad["energy_transfer_sum"])
    print("  same J0 but different J1:", triad["same_J0_different_J1"])
    print("  recovered r from J0,J1:", triad["recovered_r"])
    print("  analytic R*:", triad["analytic_Rstar"])
    print()

    print("[3D cube formal observability over F_p]")
    print("  d_M =", cube["real_state_dimension"], "shells=", cube["shells_k2"])
    print("  translation gauge upper bound =", cube["max_generic_local_rank"])
    print("  shell reader first reaches rank 49 at R =", cube["shell_first_rank49_order"])
    print("  total-energy reader first reaches rank 49 at R =", cube["total_energy_first_rank49_order"])
    print("  shell ranks R=0..24:", cube["shell_rank_0_24"])
    print("  generic-local dimension ratio 49/52 =", f"{cube['dimension_ratio_generic_local']:.6f}")

    claims = [
        {
            "id": "Vol6-NSObs-triad-Rstar1-check",
            "name": "Exact-rational triad coefficients and R=0 insufficiency witness for the analytic R*=1 subcase",
            "tier": "finite_diagnostic",
            "status": "PASS" if triad_ok else "FAIL",
            "evidence": (
                "coefficients are exact Fractions (3/10,-4/5,1/2), both nonlinear conservation sums are zero, "
                "and equal shell magnitudes with different triad phase give different J1; companion note proves closure of (x,y,z,r)"
            ),
        },
        {
            "id": "Vol6-NSObs-cube-modular-rank",
            "name": "Exact modular Taylor-readout rank witness for the 52-real-dimensional 3D cube Galerkin truncation",
            "tier": "finite_diagnostic",
            "status": "PASS" if cube_ok else "FAIL",
            "evidence": (
                f"over F_{P}, shell rank first reaches 49 at R={cube['shell_first_rank49_order']} and total-energy rank at "
                f"R={cube['total_energy_first_rank49_order']}; translation symmetry independently bounds characteristic-zero generic rank by 49"
            ),
        },
        {
            "id": "Vol6-NSObs-global-Rstar-cube",
            "name": "Global ideal-stabilization order R_M^star for the full 3D cube truncation",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "rank saturation proves generic local observability modulo translation, not global equality of polynomial fibers; "
                "a Groebner/ideal stabilization or equivalent global argument is still required"
            ),
        },
        {
            "id": "Vol6-NSObs-cost-acceleration",
            "name": "Measured reduced propagation cost C(Q_min^NS) below full 3D NS cost",
            "tier": "Open",
            "status": "OPEN",
            "evidence": (
                "the exact all-future local quotient has dimension 49/52 in this truncation and no independent 49-state reduced propagator has been built; "
                "dimension alone is not a cost certificate"
            ),
        },
    ]

    print("REPORT_JSON:" + json.dumps({"triad": triad, "cube": cube}, sort_keys=True))
    print("RESULT_JSON:" + json.dumps({"volume": 6, "claims": claims}))
    return 0 if triad_ok and cube_ok else 1


if __name__ == "__main__":
    sys.exit(main())
