#!/usr/bin/env python3
"""Exact finite checker for the shell-conditioned polarization-span obstruction.

Parent theorem:
  PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01

If q is cross-silent to every retained anchor, every anchor off the recruited
shell |q| must satisfy a_i.q=0. Hence q lies in the orthogonal complement of
the off-shell polarization span. A nonzero q therefore requires that span to
have rank at most two.

This checker records an exact shell-collision example in which the off-shell
span still has rank three for every retained shell; shell collision alone is
therefore not the exceptional mechanism.
"""

import sympy as sp


def V(*xs):
    return sp.Matrix(xs)

# Three shell radii, each repeated twice.
anchors = [
    (V(1,0,0),   V(0,1,0)),
    (V(-1,0,0),  V(0,0,1)),
    (V(0,2,0),   V(1,0,0)),
    (V(0,-2,0),  V(0,0,1)),
    (V(0,0,3),   V(1,0,0)),
    (V(0,0,-3),  V(0,1,0)),
]

# Transversality.
for p,a in anchors:
    assert p.dot(a) == 0
    assert p != sp.zeros(3,1) and a != sp.zeros(3,1)

r2_values = sorted(set(sp.expand(p.dot(p)) for p,_ in anchors), key=int)
assert r2_values == [1,4,9]

# For each retained shell, delete all anchors on that shell and check that the
# remaining polarization span is still R^3.
for rho2 in r2_values:
    off = [a for p,a in anchors if sp.expand(p.dot(p)) != rho2]
    M = sp.Matrix.hstack(*off)
    assert M.rank() == 3

# For a recruited shell not present among anchors, all anchors are off-shell.
assert sp.Matrix.hstack(*[a for _,a in anchors]).rank() == 3

# Exact linear-algebra consequence: rank-3 off-shell span has trivial
# orthogonal complement.
qx,qy,qz = sp.symbols('qx qy qz')
q = V(qx,qy,qz)
for rho2 in r2_values:
    off = [a for p,a in anchors if sp.expand(p.dot(p)) != rho2]
    # Choose an independent basis of three columns.
    basis = sp.Matrix.hstack(*off).columnspace()
    assert len(basis) == 3
    M = sp.Matrix.vstack(*[v.T for v in basis])
    assert M.det() != 0
    assert sp.linsolve((M, sp.zeros(3,1)), (qx,qy,qz)) == {(0,0,0)}

print('NS P2 shell-conditioned polarization-span obstruction: PASS')
print('shell collisions present at radii^2 1,4,9')
print('off-shell polarization span remains rank 3 for every retained shell')
print('therefore shell collision alone does not permit complete cross-silence')
