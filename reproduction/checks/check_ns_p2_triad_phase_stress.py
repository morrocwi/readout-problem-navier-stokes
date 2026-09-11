#!/usr/bin/env python3
"""Exact triad stress control for the reopened P2 mathematical attack.

Uses the analytic 2D vorticity triad embedded in 3D periodic NS already present in
check_volume6_ns_observability.py:
  a=(1,0,0), b=(1,1,0), c=(-2,-1,0)
  c_a=3/10, c_b=-4/5, c_c=1/2, nu=1/200.

Reduced variables (x,y,z,r) obey
  x' = 2 c_a r - 2 nu |a|^2 x
  y' = 2 c_b r - 2 nu |b|^2 y
  z' = 2 c_c r - 2 nu |c|^2 z
  r' = c_a y z + c_b x z + c_c x y
       - nu (|a|^2+|b|^2+|c|^2) r.

The checker establishes two exact facts relevant to scale-contraction attempts:
1) identical shell energies with opposite admissible phase coordinate r give opposite
   nonlinear transfer directions; shell energies alone are not dynamically closed.
2) the purely viscous part cancels exactly in d/dt log(|r|/sqrt(xyz)); viscosity does
   not by itself create a strict contraction of normalized triad phase coherence.

This refutes only those precise shortcuts. It does not refute a phase-complete
all-scale contraction theorem and does not make a continuum regularity claim.
"""
from fractions import Fraction

nu = Fraction(1, 200)
sa, sb, sc = 1, 2, 5
ca, cb, cc = Fraction(3,10), Fraction(-4,5), Fraction(1,2)


def rhs(x, y, z, r):
    return (
        2*ca*r - 2*nu*sa*x,
        2*cb*r - 2*nu*sb*y,
        2*cc*r - 2*nu*sc*z,
        ca*y*z + cb*x*z + cc*x*y - nu*(sa+sb+sc)*r,
    )


def main():
    assert ca + cb + cc == 0
    assert ca/Fraction(sa) + cb/Fraction(sb) + cc/Fraction(sc) == 0

    x = y = z = Fraction(1)
    plus = rhs(x,y,z,Fraction(1))
    minus = rhs(x,y,z,Fraction(-1))

    # Exact phase reversal: same shell energies, high shell c grows for r=+1
    # and decays for r=-1.
    assert plus[2] == Fraction(19,20)
    assert minus[2] == Fraction(-21,20)
    assert plus[2] > 0 > minus[2]

    # Middle shell reverses in the opposite direction as well.
    assert plus[1] == Fraction(-81,50)
    assert minus[1] == Fraction(79,50)

    # At x=y=z=1 the nonlinear part of r' cancels; only viscosity remains.
    assert plus[3] == Fraction(-1,25)
    assert minus[3] == Fraction(1,25)

    # Viscous contribution to d log |r| equals -nu(sa+sb+sc).
    visc_log_r = -nu*(sa+sb+sc)
    # Each energy has viscous log derivative -2 nu s, so half the sum is equal.
    visc_half_log_xyz = Fraction(1,2) * (-2*nu*sa - 2*nu*sb - 2*nu*sc)
    assert visc_log_r == visc_half_log_xyz
    assert visc_log_r - visc_half_log_xyz == 0

    print('NS P2 exact triad phase stress')
    print('coefficients:', ca, cb, cc)
    print('r=+1 rhs:', plus)
    print('r=-1 rhs:', minus)
    print('high-shell derivative flips sign:', plus[2], minus[2])
    print('normalized phase-coherence viscous log contribution: 0')
    print('NS-P2 TRIAD PHASE STRESS PASS')


if __name__ == '__main__':
    main()
