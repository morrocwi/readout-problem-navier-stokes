#!/usr/bin/env python3
"""Exact symbolic checker for rank-2 polarization-plane escape/rigidity.

Fix a polarization plane W=n^perp with n=e3. For a source mode p not parallel n,
any nonzero polarization a in W cap p^perp is a scalar multiple of n x p.
Likewise for q,b.

For a=alpha(n x p), b=beta(n x q), the projected NSE interaction satisfies

  n.B_{p,q}(a,b)
    = 2 alpha beta (n.(p+q)) (n.(p x q))^2 / |p+q|^2.

Moreover the unprojected source has an overall factor n.(p x q), so projected-
direction collision n.(p x q)=0 makes the pair completely nonproductive. Hence
for a productive pair whose output remains in W, n.(p+q)=0 is forced.

For three productive modes with all three pair interactions W-closed, the three
pairwise n-component sums vanish and all three modes lie in W.

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

area = sp.expand(n.dot(p.cross(q)))
raw = sp.simplify((a.dot(q))*b + (b.dot(p))*a)
out=B(p,q,a,b)

# Exact W-escape identity.
expected = sp.factor(2*al*be*n.dot(k)*area**2/k.dot(k))
assert sp.simplify(sp.factor(n.dot(out)) - expected) == 0

# Stronger fact: projected-direction collision kills the parent source itself.
raw_expected = V(
    al*be*(py-qy)*area,
    -al*be*(px-qx)*area,
    0,
)
assert sp.simplify(raw-raw_expected) == sp.zeros(3,1)
assert sp.simplify(raw.subs(px*qy-py*qx,0)) == sp.zeros(3,1)

# Therefore a productive pair (raw != 0) has area != 0. If its projected
# output remains in W, the exact escape identity forces n.(p+q)=0.

# Three-mode exact rigidity for productive W-closed pair interactions.
z1,z2,z3 = sp.symbols('z1 z2 z3', real=True)
sol = sp.solve([z1+z2, z1+z3, z2+z3], [z1,z2,z3], dict=True)
assert sol == [{z1:0,z2:0,z3:0}]

# Exact rational non-vacuity control with three pairwise nonparallel projected
# directions and a nonplanar vertical assignment: at least one pair escapes W.
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
print('projected-direction collision makes the pair nonproductive')
print('productive W-closed pair => n.(p+q)=0')
print('three productive W-closed pair interactions => all three modes lie in W')
