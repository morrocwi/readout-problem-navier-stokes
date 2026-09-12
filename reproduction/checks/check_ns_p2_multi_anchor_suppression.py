#!/usr/bin/env python3
"""Exact finite checker for the four-anchor no-silent-recruitment corollary.

Parent proposal:
  PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01

If a nonzero source mode q with one nonzero polarization b suppresses the cross
interaction against four retained anchors (p_i,a_i), then for each anchor the
parent theorem forces
    a_i.q = 0  OR  |q| = |p_i|.
If the four shell radii are pairwise distinct, the shell alternative can hold
for at most one anchor. Hence q must be orthogonal to at least three anchor
polarizations. If every triple of anchor polarizations is linearly independent,
this forces q=0, contradiction.

This file checks the finite branch logic and an exact rational non-vacuity
anchor family. No floating arithmetic is used.
"""

import itertools
import sympy as sp


def V(*xs):
    return sp.Matrix(xs)

# ---------------------------------------------------------------------------
# 1. Finite branch logic: four binary nullity alternatives.
#    S = equal-shell branch, O = polarization-orthogonality branch.
# ---------------------------------------------------------------------------
patterns = list(itertools.product("SO", repeat=4))
for pat in patterns:
    shell_count = pat.count("S")
    orth_count = pat.count("O")
    if shell_count >= 2:
        # Impossible under pairwise-distinct anchor shell radii, because one
        # |q| cannot equal two distinct |p_i| values.
        continue
    # Every remaining admissible pattern has at least three O constraints.
    assert orth_count >= 3

# ---------------------------------------------------------------------------
# 2. Exact rational anchor family showing hypotheses are non-vacuous.
# ---------------------------------------------------------------------------
p1, a1 = V(1,0,0), V(0,1,0)
p2, a2 = V(0,2,0), V(0,0,1)
p3, a3 = V(0,0,3), V(1,0,0)
p4, a4 = V(4,4,0), V(1,-1,1)
anchors = [(p1,a1),(p2,a2),(p3,a3),(p4,a4)]

# Each polarization is transverse to its anchor.
for p,a in anchors:
    assert p.dot(a) == 0
    assert p != sp.zeros(3,1)
    assert a != sp.zeros(3,1)

# Pairwise distinct squared shell radii.
r2 = [sp.expand(p.dot(p)) for p,_ in anchors]
for x,y in itertools.combinations(r2,2):
    assert sp.simplify(x-y) != 0

# Every triple of anchor polarizations is independent.
avec = [a for _,a in anchors]
for triple in itertools.combinations(avec,3):
    assert sp.Matrix.hstack(*triple).det() != 0

# Therefore any q orthogonal to any three anchor polarizations is exactly zero.
qx,qy,qz = sp.symbols("qx qy qz")
q = V(qx,qy,qz)
for triple in itertools.combinations(avec,3):
    M = sp.Matrix.vstack(*[a.T for a in triple])
    assert M.det() != 0
    sol = sp.linsolve((M, sp.zeros(3,1)), (qx,qy,qz))
    assert sol == {(0,0,0)}

print("NS P2 four-anchor suppression corollary: PASS")
print("pairwise-distinct shells => at most one equal-shell escape")
print("four silent anchors => at least three orthogonality constraints")
print("every polarization triple independent => q=0 contradiction")
