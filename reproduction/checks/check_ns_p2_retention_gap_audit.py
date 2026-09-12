#!/usr/bin/env python3
"""Exact fixtures for the audit of the 'Uniform Retention Gap' sketch (H^3 shell readouts, Duhamel window).

Objects (H^3 coordinates on the torus, mean-zero):
  shells S_j = {lambda_j <= |k| < lambda_{j+1}},  lambda_j = 2^j;
  readout  R_j^N(T) = sup_t ( sum_{k in S_j} |k|^6 |u_k^N(t)|^2 )^{1/2};
  window   tau_j = c / (nu lambda_{j+1}^2);
  old history  lambda_{j+1}^3 ||e^{nu Delta tau_j} P_{j+1} u(t - tau_j)||_2 <= e^{-c} R_{j+1};
  recent window  N_{j+1} := lambda_{j+1}^3 || int_{t-tau_j}^t e^{nu Delta (t-s)} P_{j+1} P grad.(u x u) ds ||_2;
  the one open inequality (RRB):  N_{j+1} <= alpha R_j + C 2^{-sigma j} B,  alpha < 1 - e^{-c}, sigma > 0.

All decisions are exact (Fraction / sympy Rational, e^{-c} kept as a symbol E in (0,1) where it enters algebra).
No regularity claim is made; the two directions of the equivalence sketch are not checked here.
"""

from fractions import Fraction as F
from itertools import product

import sympy as sp

# ---------------------------------------------------------------------------
# (a) Old-history factor.  For |k| >= lambda_{j+1} and tau_j = c/(nu lambda_{j+1}^2):
#     nu |k|^2 tau_j = c |k|^2 / lambda_{j+1}^2 >= c,  hence e^{-nu|k|^2 tau_j} <= e^{-c}  (exponent comparison).
#     And lambda_{j+1}^3 ||P_{j+1} u||_2 <= ( sum_{k in S_{j+1}} |k|^6 |u_k|^2 )^{1/2} = R_{j+1}  (|k| >= lambda_{j+1}).
# ---------------------------------------------------------------------------
nu_s, c_s = sp.symbols("nu c", positive=True)
for j in range(0, 6):
    lam1 = sp.Integer(2) ** (j + 1)
    tau = c_s / (nu_s * lam1 ** 2)
    for kk in ((lam1, 0, 0), (lam1, 1, 0), (lam1, lam1, lam1), (2 * lam1 - 1, 1, 1)):
        k2 = sum(x * x for x in kk)
        assert k2 >= lam1 ** 2
        exponent = nu_s * k2 * tau
        assert sp.simplify(exponent - c_s * k2 / lam1 ** 2) == 0
        assert sp.simplify(exponent - c_s) >= 0          # exact: (k2 - lam1^2) c / lam1^2 >= 0
for j, c_val, nu_val in ((0, F(1), F(1, 200)), (3, F(2), F(1, 10)), (7, F(1, 3), F(5))):
    lam1 = F(2) ** (j + 1)
    tau = c_val / (nu_val * lam1 ** 2)
    for kk in ((lam1, 0, 0), (lam1, lam1, 0), (2 * lam1 - 1, 0, 1)):
        k2 = sum(x * x for x in kk)
        assert nu_val * k2 * tau >= c_val                  # e^{-nu|k|^2 tau} <= e^{-c}, monotone exp
# lambda_{j+1}^3 ||P_{j+1} u||_2 <= R_{j+1} on an exact finite example (shell 1: 2 <= |k| < 4)
lam1 = 2
shell1 = {(2, 0, 0): F(1, 3), (2, 1, 0): F(1, 5), (3, 1, 1): F(2, 7), (2, 2, 2): F(1, 11)}
lhs2 = lam1 ** 6 * sum(a * a for a in shell1.values())
rhs2 = sum(sum(x * x for x in kk) ** 3 * a * a for kk, a in shell1.items())
assert lhs2 <= rhs2

# ---------------------------------------------------------------------------
# (b) Recurrence algebra with E := e^{-c} a symbol in (0,1).
#     (1-E) R_{j+1} <= alpha R_j + C 2^{-sigma j} B  =>  R_{j+1} <= q R_j + C' 2^{-sigma j} B,
#     q = alpha/(1-E), C' = C/(1-E);  q < 1  iff  alpha < 1-E.
# ---------------------------------------------------------------------------
E, al, C, B, Rj, Rj1, w = sp.symbols("E alpha C B R_j R_j1 w", positive=True)
q_sym = al / (1 - E)
Cp_sym = C / (1 - E)
# dividing the hypothesis by 1-E > 0 gives exactly the recurrence
assert sp.simplify((al * Rj + C * w * B) / (1 - E) - (q_sym * Rj + Cp_sym * w * B)) == 0
for E_v, a_v in ((F(1, 3), F(1, 2)), (F(1, 3), F(2, 3)), (F(1, 3), F(3, 4)), (F(9, 10), F(1, 20)), (F(9, 10), F(1, 10))):
    q_v = a_v / (1 - E_v)
    assert (q_v < 1) == (a_v < 1 - E_v)
    assert 0 < E_v < 1


def iterate_recurrence(q, Cp, B_v, r, R0, J):
    """Equality case R_{j+1} = q R_j + Cp r^j B (the maximal sequence under the recurrence)."""
    seq = [R0]
    for j in range(J):
        seq.append(q * seq[-1] + Cp * r ** j * B_v)
    return seq


def conv_bound(q, r, j):
    """Exact bound for sum_{m=0}^{j-1} q^{j-1-m} r^m with theta = max(q, r)."""
    theta = max(q, r)
    if q != r:
        return theta ** j / abs(q - r)      # (q^j - r^j)/(q - r) <= theta^j/|q - r|
    return j * theta ** (j - 1)             # q = r: exactly j theta^{j-1}


for E_v, a_v, sig, C_v, B_v, R0 in (
    (F(1, 3), F(1, 2), 1, F(2), F(1), F(1)),       # q = 3/4, r = 1/2, theta = 3/4
    (F(1, 3), F(1, 3), 1, F(1), F(3), F(2)),       # q = 1/2 = r (coincident case)
    (F(1, 2), F(1, 5), 2, F(5), F(1), F(1, 7)),    # q = 2/5, r = 1/4, theta = 2/5
    (F(1, 2), F(1, 8), 1, F(1), F(1), F(1)),       # q = 1/4 < r = 1/2, theta = 1/2
):
    q_v = a_v / (1 - E_v)
    Cp_v = C_v / (1 - E_v)
    r_v = F(1, 2) ** sig
    assert q_v < 1 and 0 < r_v < 1
    seq = iterate_recurrence(q_v, Cp_v, B_v, r_v, R0, 14)
    theta = max(q_v, r_v)
    for j in range(1, 15):
        conv = sum(q_v ** (j - 1 - m) * r_v ** m for m in range(j))
        assert seq[j] == q_v ** j * R0 + Cp_v * B_v * conv        # closed form of the iteration
        assert conv <= conv_bound(q_v, r_v, j)
        if q_v != r_v:
            C_T = R0 + Cp_v * B_v / abs(q_v - r_v)
            assert seq[j] <= C_T * theta ** j                     # R_j <= C_T theta^j
        else:
            assert seq[j] <= (R0 + Cp_v * B_v * j / theta) * theta ** j   # j theta^{j-1} growth only
    # summability of the majorant: geometric tail exact
    assert sum(theta ** j for j in range(0, 60)) < 1 / (1 - theta)
# q < 1 fails when alpha >= 1-E: the equality iteration then does not decay
q_bad = F(3, 4) / (1 - F(1, 3))
assert q_bad > 1
seq_bad = iterate_recurrence(q_bad, F(1), F(0), F(1, 2), F(1), 6)
assert all(seq_bad[j + 1] > seq_bad[j] for j in range(6))

# ---------------------------------------------------------------------------
# (c) sum_j R_j < infinity  =>  uniform homogeneous H^3.  Pointwise in t:
#     ||u||_{H^3-hom}^2 = sum_k |k|^6 |u_k|^2 = sum_j R_j(t)^2 <= ( sum_j R_j(t) )^2 <= ( sum_j sup_t R_j )^2
#     (ell^1 over shells dominates ell^2 over shells).  Exact finite example with modes in shells 0,1,2.
# ---------------------------------------------------------------------------
modes = {(1, 0, 0): F(1, 2), (1, 1, 0): F(1, 3), (2, 0, 1): F(1, 4), (3, 1, 0): F(1, 5), (4, 0, 0): F(1, 6), (5, 3, 1): F(1, 9)}


def shell_index(kk):
    k2 = sum(x * x for x in kk)
    j = 0
    while (2 ** (j + 1)) ** 2 <= k2:
        j += 1
    return j


shell_sq = {}
for kk, a in modes.items():
    shell_sq[shell_index(kk)] = shell_sq.get(shell_index(kk), F(0)) + sum(x * x for x in kk) ** 3 * a * a
h3_sq = sum(sum(x * x for x in kk) ** 3 * a * a for kk, a in modes.items())
assert h3_sq == sum(shell_sq.values())
assert sorted(shell_sq) == [0, 1, 2]
# (sum_j R_j)^2 - sum_j R_j^2 = 2 sum_{i<j} R_i R_j >= 0: the shell readouts R_j = sqrt(shell_sq[j]) are kept
# as exact sympy square roots of rationals; the cross-term sum is a sum of positive square roots.
R_sym = [sp.sqrt(sp.Rational(shell_sq[j].numerator, shell_sq[j].denominator)) for j in (0, 1, 2)]
cross_terms = sp.expand(sum(R_sym) ** 2) - sum(r ** 2 for r in R_sym)
assert sp.simplify(cross_terms - 2 * (R_sym[0] * R_sym[1] + R_sym[1] * R_sym[2] + R_sym[0] * R_sym[2])) == 0
assert cross_terms.is_positive                               # exact: each product of square roots is positive
assert sp.simplify(sum(r ** 2 for r in R_sym) - sp.Rational(h3_sq.numerator, h3_sq.denominator)) == 0
# the symbolic identity behind it
a_, b_, c_ = sp.symbols("a b c", nonnegative=True)
assert sp.expand((a_ + b_ + c_) ** 2 - (a_ ** 2 + b_ ** 2 + c_ ** 2) - 2 * (a_ * b_ + b_ * c_ + c_ * a_)) == 0

# ---------------------------------------------------------------------------
# (d) THE REFUTATION of an energy-only remainder.  t = 0 window-level ratio proxy
#        N_{j0+1} ~ tau_{j0} * rate,   rate^2 := sum_{k in S_{j0+1}} |k|^6 |F_k|^2,   F = P grad.(u x u),
#     (first order in the window: the t=0 H^3-shell rate times the window length -- a lower-order proxy for the
#     Duhamel integral, NOT the windowed quantity itself), against R_{j0}^2 = sum_{k in S_{j0}} |k|^6 |a_k|^2.
#     Datum families (real field a_{-k} = a_k, div-free a_k . k = 0, common scalar amplitude c, energy E_0):
#       A  cube surface  |k|_inf = lambda_0 (so |k| in [lambda_0, sqrt3 lambda_0) subset S_{j0}; ~lambda_0^2 modes),
#          polarization e_k = k x e_axis (axis of least |k_i|), e_{-k} = e_k;
#       B  full dyadic shell  lambda_0 <= |k| < 2 lambda_0  (~lambda_0^3 modes), same cross polarization;
#       C  full dyadic shell, coherent polarization a_k = (I - k k^T/|k|^2) e_z (Leray-projected uniform field,
#          constructive at x = 0), scaled by lcm(|k|^2) to integers;
#       D  few-mode: +-lambda_0 (1,0,0) with e = (0,1,0) and +-lambda_0 (1,1,0) with e = (0,0,1).
#     Amplitudes are NOT equal mode by mode (|e_k| varies within a factor < 2 in A/B; C has |a_k|^2 = 1 - k_z^2/|k|^2);
#     the single scalar c fixes the total energy.
#     Bilinear term by exact integer triad convolution:
#        F_k = i (I - k k^T/|k|^2) v_k,   v_k = sum_{k'} (a_{k'} . k) a_{k-k'}   (div-free: a_{k'}.(k-k') = a_{k'}.k).
#     With a_k = c e_k:  rate^2 = c^4 S_F,  R^2 = c^2 S_R,  E_0 = c^2 S_E,  tau = c_w/(nu lambda_{j0+1}^2), so
#        (N/R)^2 = (c_w^2 E_0 / nu^2) * G,   G := S_F / (S_R S_E lambda_{j0+1}^4)   -- a pure lattice number,
#     invariant under a common integer rescaling of the e_k.  Bernstein saturation ||u||_inf ~ lambda^{3/2} ||u||_2
#     predicts G ~ lambda_0 (ratio ~ sqrt(lambda_0)); this is the analytic (Dr) part, not checked here.
# ---------------------------------------------------------------------------
from math import lcm

import numpy as np


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def modes_cube(lam0):
    rng = range(-lam0, lam0 + 1)
    return [kk for kk in product(rng, rng, rng) if max(abs(x) for x in kk) == lam0]


def modes_dyadic(lam0):
    rng = range(-2 * lam0 + 1, 2 * lam0)
    return [kk for kk in product(rng, rng, rng) if lam0 ** 2 <= dot(kk, kk) < 4 * lam0 ** 2]


def pol_cross(ks):
    """e_k = k x e_axis with axis = argmin |k_i| on the sign representative; e_{-k} = e_k."""
    pol = {}
    for kk in ks:
        rep = kk if [x for x in kk if x != 0][0] > 0 else tuple(-x for x in kk)
        axis = min(range(3), key=lambda i: (abs(rep[i]), i))
        e = cross(rep, tuple(1 if i == axis else 0 for i in range(3)))
        assert dot(e, kk) == 0 and e != (0, 0, 0)
        pol[kk] = e
    return pol


def pol_leray_z(ks):
    """a_k = |k|^2 e_z - k_z k, times lcm(|k|^2)/|k|^2 (integer form of (I - k k^T/|k|^2) e_z); even in k."""
    L = 1
    for kk in ks:
        L = lcm(L, dot(kk, kk))
    pol = {}
    for kk in ks:
        k2 = dot(kk, kk)
        s = L // k2
        e = (-s * kk[2] * kk[0], -s * kk[2] * kk[1], s * (k2 - kk[2] * kk[2]))
        assert dot(e, kk) == 0
        pol[kk] = e                                   # e = 0 exactly for k parallel to e_z
    return pol


def few_mode_datum(lam0):
    pol = {}
    for kk, e in (((lam0, 0, 0), (0, 1, 0)), ((lam0, lam0, 0), (0, 0, 1))):
        pol[kk] = e
        pol[tuple(-x for x in kk)] = e
        assert dot(e, kk) == 0
    return pol


def shell_sums(pol, j0):
    lam0, lam1 = 2 ** j0, 2 ** (j0 + 1)
    S_R = 0
    S_E = 0
    for kk, e in pol.items():
        k2 = dot(kk, kk)
        assert lam0 ** 2 <= k2 < lam1 ** 2            # datum lives in shell j0
        S_R += k2 ** 3 * dot(e, e)
        S_E += dot(e, e)
    return S_R, S_E


def finish(v, S_R, S_E, j0):
    """From the accumulated v_k on shell j0+1 return (S_F, S_R, S_E, G, G_lam, targets)."""
    lam1 = 2 ** (j0 + 1)
    S_F = F(0)
    S_F2 = F(0)
    nt = 0
    for kk, vv in v.items():
        if vv == (0, 0, 0):
            continue
        k2 = dot(kk, kk)
        proj2 = F(dot(vv, vv)) - F(dot(kk, vv) ** 2, k2)   # |(I - P_k) v|^2
        S_F += k2 ** 3 * proj2
        S_F2 += proj2
        nt += 1
    G = S_F / (S_R * S_E * F(lam1) ** 4)
    G_lam = F(lam1) ** 6 * S_F2 / (S_R * S_E * F(lam1) ** 4)   # variant with lambda_{j0+1}^3 ||P_{j0+1} F||_2
    return S_F, S_R, S_E, G, G_lam, nt


def window_factor_py(pol, j0):
    """Pure-Python big-integer triad convolution onto shell j0+1."""
    lam1, lam2 = 2 ** (j0 + 1), 2 ** (j0 + 2)
    S_R, S_E = shell_sums(pol, j0)
    v = {}
    items = list(pol.items())
    for kp, ep in items:
        for kpp, epp in items:
            kk = (kp[0] + kpp[0], kp[1] + kpp[1], kp[2] + kpp[2])
            k2 = dot(kk, kk)
            if not (lam1 ** 2 <= k2 < lam2 ** 2):
                continue                             # keep only targets in shell j0+1
            coef = dot(ep, kk)                       # (a_{k'} . k)
            if coef == 0:
                continue
            cur = v.get(kk, (0, 0, 0))
            v[kk] = (cur[0] + coef * epp[0], cur[1] + coef * epp[1], cur[2] + coef * epp[2])
    return finish(v, S_R, S_E, j0)


def window_factor_np(pol, j0, e_bound):
    """Same convolution vectorised in int64; exact because every partial sum is bounded a priori below 2^62."""
    lam1, lam2 = 2 ** (j0 + 1), 2 ** (j0 + 2)
    S_R, S_E = shell_sums(pol, j0)
    n = len(pol)
    # |coef| <= sum_i |e_i| |T_i| <= 3 e_bound (lam2 - 1), |coef e''_i| <= 3 e_bound^2 lam2, at most n terms per target
    assert 3 * e_bound ** 2 * lam2 * n < 2 ** 62
    K = np.array(list(pol.keys()), dtype=np.int64)
    Ev = np.array(list(pol.values()), dtype=np.int64)
    assert int(np.abs(Ev).max()) <= e_bound
    off = lam2
    size = 2 * lam2 + 1
    V = np.zeros((size, size, size, 3), dtype=np.int64)
    for i in range(n):
        T = K[i] + K
        t2 = (T * T).sum(1)
        m = (t2 >= lam1 * lam1) & (t2 < lam2 * lam2)
        if not m.any():
            continue
        Tm = T[m]
        coef = (Ev[i] * Tm).sum(1)
        idx = Tm + off
        np.add.at(V, (idx[:, 0], idx[:, 1], idx[:, 2]), coef[:, None] * Ev[m])
    v = {}
    for ix in np.argwhere((V != 0).any(3)):
        v[tuple(int(x) - off for x in ix)] = tuple(int(x) for x in V[tuple(ix)])
    return finish(v, S_R, S_E, j0)


# D: few-mode closed form  S_F = 250 lam0^8, S_R = 18 lam0^6, S_E = 4, G = 250/(72*16) lam0^{-2}, G_lam = lam0^{-2}/9
few = {}
for j0 in (0, 1, 2, 3):
    lam0 = 2 ** j0
    few[lam0] = window_factor_py(few_mode_datum(lam0), j0)
    S_F, S_R, S_E, G, G_lam, nt = few[lam0]
    assert nt == 2 and S_F == 250 * lam0 ** 8 and S_R == 18 * lam0 ** 6 and S_E == 4
    assert G == F(250, 72 * 16) / lam0 ** 2 and G_lam == F(1, 9) / lam0 ** 2
few_seq = [few[l][3] for l in (1, 2, 4, 8)]
assert all(few_seq[i + 1] == few_seq[i] / 4 for i in range(3))            # DECREASES, exactly lambda_0^{-2}

# A: cube surface, cross polarization (the datum as first sketched): ~lambda_0^2 modes, NOT Bernstein-saturating
cubeA = {}
for j0 in (0, 1, 2):
    lam0 = 2 ** j0
    cubeA[lam0] = window_factor_py(pol_cross(modes_cube(lam0)), j0)
assert [len(modes_cube(l)) for l in (1, 2, 4)] == [26, 98, 386]           # 3^3-1, 5^3-3^3, 9^3-7^3
cubeA_seq = [cubeA[l][3] for l in (1, 2, 4)]
assert all(cubeA_seq[i + 1] < cubeA_seq[i] for i in range(2))             # DECREASES with lambda_0

# B: full dyadic shell, cross polarization, lambda_0 = 1, 2, 4 (pure Python) and 8 (int64, cross-checked <= 4)
dyadB = {}
for j0 in (0, 1, 2, 3):
    lam0 = 2 ** j0
    pol = pol_cross(modes_dyadic(lam0))
    e_bound = 2 * lam0                                # |e_k| <= |k| < 2 lambda_0 componentwise
    res_np = window_factor_np(pol, j0, e_bound)
    if lam0 <= 4:
        res_py = window_factor_py(pol, j0)
        assert res_py[:5] == res_np[:5]               # exact agreement of the two evaluation paths
    dyadB[lam0] = res_np
assert [len(modes_dyadic(l)) for l in (1, 2, 4, 8)] == [26, 224, 1852, 14968]
dyadB_seq = [dyadB[l][3] for l in (1, 2, 4, 8)]
assert all(dyadB_seq[i + 1] > dyadB_seq[i] for i in range(3))             # INCREASES with lambda_0
dyadB_step = [dyadB_seq[i + 1] / dyadB_seq[i] for i in range(3)]
assert all(dyadB_step[i + 1] > dyadB_step[i] for i in range(2))           # step ratio itself increasing (toward 2)
assert dyadB_step[2] > F(3, 2)

# C: full dyadic shell, coherent Leray-z polarization, lambda_0 = 1, 2, 4 (big-int pure Python)
dyadC = {}
for j0 in (0, 1, 2):
    lam0 = 2 ** j0
    dyadC[lam0] = window_factor_py(pol_leray_z(modes_dyadic(lam0)), j0)
dyadC_seq = [dyadC[l][3] for l in (1, 2, 4)]
assert all(dyadC_seq[i + 1] > dyadC_seq[i] for i in range(2))             # INCREASES with lambda_0
assert dyadC_seq[2] / dyadC_seq[1] > F(3, 2)

# Coherence readout |sum_k e_k|^2 / sum_k |e_k|^2 (= |u(0)|^2 / (c^2 S_E); N for a fully coherent datum)
def coherence(pol):
    s = (0, 0, 0)
    for e in pol.values():
        s = (s[0] + e[0], s[1] + e[1], s[2] + e[2])
    return F(dot(s, s), sum(dot(e, e) for e in pol.values()))


# Amplitude spread of the cross polarization (paper section 3), exact on |e_k|^2:
#   A: max/min = 2 at every lambda_0 (|e|^2 = lambda_0^2 at (lambda_0,0,0), 2 lambda_0^2 at (lambda_0,lambda_0,lambda_0));
#   B: max/min = 2, 13/4, 61/13, 5 at lambda_0 = 1, 2, 4, 8  (so |e_k| varies by up to sqrt(5) ~ 2.24, NOT < 2).
for l, ratio_B in ((1, F(2)), (2, F(13, 4)), (4, F(61, 13)), (8, F(5))):
    sqA = [dot(e, e) for e in pol_cross(modes_cube(l)).values()]
    assert F(max(sqA), min(sqA)) == 2
    sqB = [dot(e, e) for e in pol_cross(modes_dyadic(l)).values()]
    assert F(max(sqB), min(sqB)) == ratio_B
cohB = {l: coherence(pol_cross(modes_dyadic(l))) for l in (1, 2, 4)}
cohC = {l: coherence(pol_leray_z(modes_dyadic(l))) for l in (1, 2, 4)}
assert all(cohC[l] > cohB[l] for l in (1, 2, 4))                          # Leray-z is the more coherent family
# What is refuted: with G > 0 on every instance and (N/R)^2 = (c_w^2 E_0/nu^2) G, an energy-only remainder
# N_{j0+1} <= alpha R_{j0} + C 2^{-sigma j0} B(E_0, nu, T) would need G <= (alpha + C 2^{-sigma j0} B/R_{j0})^2 nu^2/(c_w^2 E_0)
# with R_{j0}^2 = E_0 S_R/S_E growing like lambda_0^6 E_0 (checked below), i.e. a bound on G that decays in j0 at
# fixed alpha, C, sigma, B, E_0, nu -- while G increases along family B/C.  This is a statement about the proxy.
for l in (1, 2, 4, 8):
    S_F, S_R, S_E = dyadB[l][:3]
    assert F(S_R, S_E) >= l ** 6                       # R_{j0}^2 / E_0 = S_R/S_E >= lambda_0^6
    assert dyadB[l][3] > 0

# ---------------------------------------------------------------------------
# (e) The two directions of the equivalence sketch (RRB <=> regularity) are not exactly checkable here.
#     Nothing is asserted about them.
# ---------------------------------------------------------------------------

print("NS P2 retention-gap audit")
print("(a) old-history factor: nu|k|^2 tau_j >= c for |k| >= lambda_{j+1}; lambda^3||P u|| <= R exact")
print("(b) recurrence: q = alpha/(1-E) < 1 iff alpha < 1-E; R_j <= C_T theta^j (q != 2^-sigma), j theta^{j-1} if equal")
print("(c) sum_j R_j < inf => sup_t ||u||_{H^3-hom} <= sum_j R_j (ell^1 >= ell^2 over shells), exact example")
print("(d) window ratio factor G = S_F/(S_R S_E lambda_{j0+1}^4), (N/R)^2 = (c_w^2 E_0/nu^2) G  [t=0 rate x window proxy]:")
for l in (1, 2, 4):
    S_F, S_R, S_E, G, G_lam, nt = cubeA[l]
    print(f"    A cube |k|_inf={l} cross: modes={len(modes_cube(l))} targets={nt} G={G} (~{float(G):.5g}) G_lam~{float(G_lam):.5g}  DECREASES")
for l in (1, 2, 4, 8):
    S_F, S_R, S_E, G, G_lam, nt = dyadB[l]
    print(f"    B dyadic lambda_0={l} cross: modes={len(modes_dyadic(l))} targets={nt} S_F={S_F} S_R={S_R} S_E={S_E}")
    print(f"      G={G} (~{float(G):.5g}) G_lam~{float(G_lam):.5g}  INCREASES")
print(f"    B step ratios G(2l)/G(l): {[round(float(g), 4) for g in dyadB_step]} (analytic Bernstein prediction 2)")
for l in (1, 2, 4):
    S_F, S_R, S_E, G, G_lam, nt = dyadC[l]
    print(f"    C dyadic lambda_0={l} Leray-z: targets={nt} G={G} (~{float(G):.5g}) G_lam~{float(G_lam):.5g} coherence~{float(cohC[l]):.4g}/{len(modes_dyadic(l))}  INCREASES")
print(f"    C step ratios: {[round(float(dyadC_seq[i + 1] / dyadC_seq[i]), 4) for i in range(2)]}")
for l in (1, 2, 4, 8):
    print(f"    D few-mode lambda_0={l}: G={few[l][3]} (~{float(few[l][3]):.5g})  DECREASES exactly lambda_0^-2")
print("(e) equivalence directions: not checked, nothing asserted")
print("NS-P2 RETENTION GAP AUDIT PASS")
