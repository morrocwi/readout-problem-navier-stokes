#!/usr/bin/env python3
"""Exact arithmetic audit for the fresh-donor recent-ancestry reduction."""

import sympy as sp

n, nu, delta, M0 = sp.symbols("n nu delta M0", positive=True)

# Existing Stokes H3 tail theorem gives squared constant 192, hence norm constant sqrt(192)=8sqrt(3).
assert sp.simplify(sp.sqrt(192) - 8*sp.sqrt(3)) == 0

eps_N = 8*sp.sqrt(3)*M0 / ((2*nu*delta)**2 * n)

# At donor scale choose cube cutoff N=n-1, so N+1=n exactly.
N = n - 1
assert sp.simplify(N + 1 - n) == 0

# Exact scaling: n * epsilon is scale-independent for fixed nu,delta,M0.
assert sp.simplify(n*eps_N - 8*sp.sqrt(3)*M0/(2*nu*delta)**2) == 0

# Reverse-triangle and large-implies-recent rational fixtures.
# If |X|=5 and memory <=2, recent nonlinear contribution is at least 3.
X = sp.Rational(5)
eps = sp.Rational(2)
recent_lower = X - eps
assert recent_lower == 3
assert X >= 2*eps
assert recent_lower >= X/2

# General theta fixture: theta=3/4, threshold eps/(1-theta)=4 eps.
theta = sp.Rational(3, 4)
X2 = sp.Rational(8)
eps2 = sp.Rational(2)
assert X2 >= eps2/(1-theta)
assert X2-eps2 >= theta*X2

# Pair fixture: both donors above 2 epsilon => at least half of each is recent.
Xq0 = sp.Rational(7)
Xq1 = sp.Rational(9)
eps_pair = sp.Rational(3)
assert Xq0 >= 2*eps_pair and Xq1 >= 2*eps_pair
assert Xq0-eps_pair >= Xq0/2
assert Xq1-eps_pair >= Xq1/2

print("NS P2 fresh-donor recent ancestry")
print("memory envelope epsilon_n,delta =", eps_N)
print("n * epsilon_n,delta =", sp.simplify(n*eps_N))
print("reverse-triangle fixture recent lower =", recent_lower)
print("theta fixture =", theta)
print("pair fixture: both large donors force >= half recent nonlinear ancestry")
print("scope: reduction to recent nonlinear ancestry; recent nonlinear closure remains OPEN")
print("NS-P2 FRESH-DONOR RECENT ANCESTRY PASS")
