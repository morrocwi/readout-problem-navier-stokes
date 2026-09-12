#!/usr/bin/env python3
"""Exact checker for rank-2 self-closure -> planarity/escape.

Parents:
- productive-triad exact self-closure lemma (existing P2 Standalone)
- PROP-P3-RANK2-POLARIZATION-PLANE-RIGIDITY-01

For W=n^perp, a productive triad p+q=k whose retained polarizations a,b,c all
lie in W and whose parent output is W-closed has k in W. The self-closure lemma
forces at least one of (p,k) or (q,k) to interact nontrivially. If that nonzero
self-closure output also stays in W, rank-2 pair rigidity forces the associated
parent mode into W, and then the other parent also lies in W. Otherwise there
is immediate polarization escape from W.

All explicit controls are exact rational arithmetic.
"""

import sympy as sp


def V(*xs):
    return sp.Matrix(xs)


def proj(w,k):
    return sp.simplify(w - (w.dot(k)/k.dot(k))*k)


def B(p,q,a,b):
    k=p+q
    return sp.simplify(proj((a.dot(q))*b + (b.dot(p))*a, k))

n=V(0,0,1)

# ---------------------------------------------------------------------------
# 1. Scalar implication behind the corollary.
# ---------------------------------------------------------------------------
zp,zq,zk = sp.symbols('zp zq zk', real=True)
# Parent W-closure in the productive rank-2 branch forces zk=zp+zq=0.
# A nonzero W-closed self-closure pair (p,k) forces zp+zk=0; similarly for q.
sol_p = sp.solve([zk-(zp+zq), zk, zp+zk], [zp,zq,zk], dict=True)
sol_q = sp.solve([zk-(zp+zq), zk, zq+zk], [zp,zq,zk], dict=True)
assert sol_p == [{zp:0,zq:0,zk:0}]
assert sol_q == [{zp:0,zq:0,zk:0}]

# ---------------------------------------------------------------------------
# 2. Exact rational non-vacuity control: productive parent is W-closed while
#    both self-closure descendants escape W.
# ---------------------------------------------------------------------------
p=V(1,0,1)
q=V(0,2,-1)
k=p+q
assert k == V(1,2,0)

a=n.cross(p)
b=n.cross(q)
parent=B(p,q,a,b)
assert parent == V(sp.Rational(-12,5), sp.Rational(6,5), 0)
assert parent != sp.zeros(3,1)
assert n.dot(parent) == 0
assert p.dot(a)==0 and q.dot(b)==0 and k.dot(parent)==0
assert n.dot(a)==0 and n.dot(b)==0

# Use the nonzero parent response itself as the k-polarization c. Then
# <c,B_{p,q}(a,b)>=||parent||^2>0, so the existing self-closure lemma applies.
c=parent
assert sp.simplify(c.dot(parent)) > 0

Dpk=B(p,k,a,c)
Dqk=B(q,k,b,c)
assert Dpk != sp.zeros(3,1) or Dqk != sp.zeros(3,1)
# In this nonplanar example both escape the common polarization plane W.
assert sp.simplify(n.dot(Dpk)) != 0
assert sp.simplify(n.dot(Dqk)) != 0

print('NS P2 rank-2 self-closure planarity/escape: PASS')
print('productive W-closed parent + retained self-closure => W escape OR p,q,k all in W')
print('exact rational example has productive W-closed parent and both self-closure descendants escaping W')
