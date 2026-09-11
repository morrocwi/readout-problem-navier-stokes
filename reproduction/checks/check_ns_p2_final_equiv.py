#!/usr/bin/env python3
from fractions import Fraction

# Exact algebra controls for the P2 final closure note.
# These checks validate the dyadic contraction algebra only; they do not prove NSE regularity.

# Direction A calibration: regularity gives R_j <= C/Lambda_j and dyadic Lambda multiplies by 4.
C = Fraction(37, 5)
Lambda0 = Fraction(9, 7)
U = []
for j in range(10):
    Lam = Lambda0 * (4 ** j)
    U.append(C / Lam)
for j in range(9):
    assert U[j + 1] == Fraction(1, 4) * U[j]

# Direction B recurrence control: kappa,rho<1 with geometric remainder forces decay.
kappa = Fraction(1, 3)
rho = Fraction(1, 2)
B = Fraction(7, 11)
u = Fraction(5, 1)
vals = [u]
for j in range(40):
    u = kappa * u + B * (rho ** j)
    vals.append(u)
assert vals[-1] < Fraction(1, 10000)
assert all(x >= 0 for x in vals)

# Critical falsifier: constant critical ratio R_j=1 cannot be bounded by a zero-remainder
# strict contraction U_{j+1} <= kappa U_j with U_j=1 and kappa<1.
critical = Fraction(1, 1)
for kappa_test in [Fraction(1, 2), Fraction(3, 4), Fraction(99, 100)]:
    assert not (critical <= kappa_test * critical)

print('NS P2 FINAL EQUIVALENCE ALGEBRA PASS')
print('regularity calibration: U_{j+1} = (1/4) U_j')
print('strict recurrence calibration: U_j -> 0')
print('critical constant-ratio zero-remainder contraction: rejected')
