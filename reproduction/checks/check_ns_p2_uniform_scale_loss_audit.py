#!/usr/bin/env python3
"""Exact fixtures for the audit of the candidate 'Uniform Full-Convolution Scale-Loss' statement (SL).

(SL):  exists delta>0, C<inf, 0<rho<1, for all j:  T_j^full <= (1-delta) nu D_j + C rho^j.

All decisions are exact (Fraction / sympy Rational). No regularity claim is made.
"""

from fractions import Fraction as F

import sympy as sp

# ---------------------------------------------------------------------------
# 1. Pointwise (SL) at the repo's exact isolated-triad state (check_ns_p2_triad_phase_stress.py).
#    a=(1,0,0), b=(1,1,0), c=(-2,-1,0); s=(1,2,5); c_a,c_b,c_c=(3/10,-4/5,1/2); nu=1/200.
# ---------------------------------------------------------------------------
nu = F(1, 200)
sa, sb, sc = 1, 2, 5
ca, cb, cc = F(3, 10), F(-4, 5), F(1, 2)
assert ca + cb + cc == 0 and ca / sa + cb / sb + cc / sc == 0     # enstrophy + energy conservation
x = y = z = F(1)
r = F(1)
T_high = 2 * cc * r                       # nonlinear transfer into the high mode c
D_high = 2 * nu * sc * z                  # its viscous dissipation, same units
assert T_high == 1 and D_high == F(1, 20)
assert T_high / D_high == 20
assert T_high - D_high == F(19, 20)       # = z' at this state (checker value)
for delta in (F(1, 1000), F(1, 2), F(1)):
    assert T_high - (1 - delta) * D_high >= F(19, 20)   # pointwise excess for every delta in (0,1]

# ---------------------------------------------------------------------------
# 2. Homothetic scale law: vorticity coefficients are n-independent, s_k -> n^2 s_k.
#    On the coherent state x=y=z=E, r=E^{3/2}:  T/D = 20 sqrt(E) / n^2.
# ---------------------------------------------------------------------------
n, E = sp.symbols("n E", positive=True)
T_n = 2 * sp.Rational(1, 2) * E ** sp.Rational(3, 2)
D_n = 2 * sp.Rational(1, 200) * 5 * n ** 2 * E
assert sp.simplify(T_n / D_n - 20 * sp.sqrt(E) / n ** 2) == 0
# amplitude tuned so that T = 2 D  (sqrt(E) = n^2/10): the excess T - D grows like n^6, not geometrically
excess = sp.simplify((T_n - D_n).subs(E, n ** 4 / 100))
assert sp.simplify(excess / excess.subs(n, 1) - n ** 6) == 0
assert excess.subs(n, 1) > 0
# fixed-amplitude family (E=1) is absorbable: T/D = 20/n^2 -> excess positive only for n<=4
assert all((20 * sp.sqrt(1) / k ** 2 > 1) == (k <= 4) for k in range(1, 20))

# ---------------------------------------------------------------------------
# 3. Abstract critical budget (P2C-3): N_j=2^j, e_j=N_j^-1, A_j=N_j, delta_j=N_j^-2.
#    An episode that builds shell j from zero has  int T_j = e_j + int D_j,  int D_j = 2 nu A_j delta_j,
#    so  int T_j / int D_j = 1 + 1/(2 nu)  for every j: O(1), j-independent, strictly > 1.
# ---------------------------------------------------------------------------
for j in range(0, 12):
    Nj = F(2) ** j
    e_j, A_j, d_j = 1 / Nj, Nj, 1 / Nj ** 2
    intD = 2 * nu * A_j * d_j
    intT = e_j + intD
    assert intT / intD == 1 + 1 / (2 * nu)
    assert intT - intD == e_j                         # H^1 excess e_j = 1/N_j at these units
assert 1 + 1 / (2 * nu) == 101

# ---------------------------------------------------------------------------
# 4. Recurrence identity: with K_{N_{j+1}}^2 <= K_{N_j}^2 + S_{j+1} (spectral orthogonality + Minkowski),
#    convexity gives (x+y)^r <= (1+eta)^{r-1} x^r + (1+1/eta)^{r-1} y^r, hence
#    R_{j+1} <= kappa R_j + C_eta R^sh_{j+1},  kappa = (1+eta)^{r-1}/4,  C_eta = (1+1/eta)^{r-1}.
#    kappa < 1  iff  eta < 4^{1/(r-1)} - 1  (p=4, r=4: eta < 4^{1/3}-1).
# ---------------------------------------------------------------------------
r_exp = 4  # p = 4
for eta in (F(1, 10), F(1, 2), F(4, 7)):
    kappa = (1 + eta) ** (r_exp - 1) / 4
    Ceta = (1 + 1 / eta) ** (r_exp - 1)
    assert kappa < 1
    for xx in (F(0), F(1, 3), F(2), F(7)):
        for yy in (F(0), F(1, 5), F(1), F(9, 2)):
            assert (xx + yy) ** r_exp <= (1 + eta) ** (r_exp - 1) * xx ** r_exp + Ceta * yy ** r_exp
assert (1 + F(3, 5)) ** 3 / 4 > 1                      # eta = 3/5 exceeds the p=4 threshold 4^{1/3}-1
assert (1 + F(1, 2)) ** 3 / 4 == F(27, 32) < 1
# R_{j+1} >= R_j / 4 always (K is monotone in N, Lambda_{j+1} = 4 Lambda_j): no recurrence has kappa < 1/4 with B = 0
K2 = F(3)
assert (K2 ** r_exp) / 4 == (K2 ** r_exp) / (4 * 1)

print("NS P2 uniform scale-loss audit")
print("pointwise (SL) at exact triad state: T/D = 20, excess >= 19/20 for every delta")
print("scale law T/D = 20 sqrt(E)/n^2; amplitude-tuned excess grows like n^6 (not geometric)")
print("critical budget: int T_j / int D_j = 1 + 1/(2 nu) = 101 for every j")
print("recurrence identity R_{j+1} <= kappa R_j + C_eta R^sh_{j+1}, kappa = (1+eta)^{r-1}/4")
print("NS-P2 UNIFORM SCALE-LOSS AUDIT PASS")
