#!/usr/bin/env python3
"""Exact symbolic checker for rank-2 polarization-plane escape/rigidity.

Fix a polarization plane W=n^perp with n=e3. For a source mode p not parallel n,
any nonzero polarization a in W cap p^perp is a scalar multiple of n x p.
Likewise for q,b.

For a=alpha(n x p), b=beta(n x q), the projected NSE interaction satisfies

  n.B_{p,q}(a,b)
    = 2 alpha beta (n.(p+q)) (n.(p x q))^2 / |p+q|^2.

Hence if the output polarization stays in W and the projected directions of p,q
are nonparallel, then n.(p+q)=0. For three modes with pairwise nonparallel
projected directions, W-closure of all three pair interactions forces all three
n-components to vanish, so the wavevectors themselves lie in W.

All checks are exact SymPy identities; no floats are used.
"""

import sympy as sp

px,py,pz,qx,qy,qz,al,be = sp.symbols(
    'px py pz qx qy qz alpha beta', real=True)


def V(*xs):
    return sp.Matrix(xs)


def proj(w,k):
    return sp.simplify(w - (w.dot(k)/k.dot(k))*k)


def B(p,q,a,b):
    k=p+q
    return sp.simplify(proj((a.dot(q))*b + (b.dot(p))*a, k))

n=V(0,0,1)
p=V(px,py,pz)
q=V(qx,qy,qz)
a=al*n.cross(p)
b=be*n.cross(q)
k=p+q

assert sp.simplify(n.dot(a)) == 0
assert sp.simplify(n.dot(b)) == 0
assert sp.simplify(p.dot(a)) == 0
assert sp.simplify(q.dot(b)) == 0

out=B(p,q,a,b)
area = sp.expand(n.dot(p.cross(q)))
expected = sp.factor(2*al*be*n.dot(k)*area**2/k.dot(k))
assert sp.simplify(sp.factor(n.dot(out)) - expected) == 0

# Three-mode exact rigidity in the generic projected-direction branch.
z1,z2,z3 = sp.symbols('z1 z2 z3', real=True)
# W-closure plus pairwise nonparallel projections implies pairwise z-sum zero.
sol = sp.solve([z1+z2, z1+z3, z2+z3], [z1,z2,z3], dict=True)
assert sol == [{z1:0,z2:0,z3:0}]

# Exact rational non-vacuity control with three pairwise nonparallel projected
# directions and one nonplanar vertical assignment: at least one pair escapes W.
ps = [V(1,0,1), V(0,1,-1), V(1,1,1)]
as_ = [n.cross(r) for r in ps]
for r,a_r in zip(ps,as_):
    assert r.dot(a_r)==0 and n.dot(a_r)==0 and a_r!=sp.zeros(3,1)

escape_count=0
for i in range(3):
    for j in range(i+1,3):
        area_ij = n.dot(ps[i].cross(ps[j]))
        assert area_ij != 0
        o=B(ps[i],ps[j],as_[i],as_[j])
        if sp.simplify(n.dot(o)) != 0:
            escape_count += 1
assert escape_count >= 1

print('NS P2 rank-2 polarization-plane rigidity: PASS')
print('n.B = 2 alpha beta (n.(p+q)) (n.(p x q))^2 / |p+q|^2')
print('three pairwise nonparallel projected directions + W-closed pair outputs => all modes planar in W')
