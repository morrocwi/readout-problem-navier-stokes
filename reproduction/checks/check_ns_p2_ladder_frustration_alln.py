#!/usr/bin/env python3
"""Symbolic exact derivation of an all-n Fourier-ladder H3 sign-frustration family.

For every positive integer n consider the real divergence-free coordinate family
  p  = (0,0,1)       : e1_re  -> a
  k- = (n,-n,-1)     : e1_im  -> b
  k0 = (n,-n,0)      : e1_re  -> c
  k0 = (n,-n,0)      : e2_re  -> d
  k+ = (n,-n,1)      : e1_im  -> e
using the same unnormalised divergence-free basis convention as
check_volume6_ns_observability.py.

The script reconstructs the Fourier bilinear interaction and Leray projection in
SymPy, forms the inhomogeneous H3 nonlinear-production coefficients, and proves
symbolically that the four cubic coefficients are

  A_n, -B_n, A_n, B_n

with
  A_n = n^3 (4 n^4 - 6 n^2 - 17)
  B_n = 2 n^3 (4 n^6 - 6 n^2 - 7).

For integer n>=1 both factors are nonzero, hence the coefficient-sign product is
-A_n^2 B_n^2 < 0.  Therefore these four monomials cannot be simultaneously sign
aligned at any cutoff in this parameterized family.

This is an all-n algebraic motif theorem, not a boundary-coverage theorem and not
a quantitative global contraction theorem.
"""
import itertools
import sympy as sp

n = sp.symbols('n', positive=True, integer=True)


def cross(a,b):
    return sp.Matrix(a).cross(sp.Matrix(b))


def basis(k):
    kv=sp.Matrix(k)
    # All modes in this declared family have nonzero cross product with e_x.
    e1=kv.cross(sp.Matrix((1,0,0)))
    if e1 == sp.zeros(3,1):
        raise AssertionError('declared family unexpectedly parallel to e_x')
    e2=kv.cross(e1)
    return e1,e2,sp.expand(e1.dot(e1)),sp.expand(e2.dot(e2))


def field(rep,slot,sgn):
    e1,e2,_,_=basis(rep)
    v=e1 if slot.startswith('e1') else e2
    if slot.endswith('im'):
        return sp.zeros(3,1), sgn*v
    return v,sp.zeros(3,1)


def same_vec(a,b):
    return all(sp.simplify(a[i]-b[i]) == 0 for i in range(3))


def bilinear_coordinate(out_rep,out_slot,r1,s1,r2,s2):
    out=sp.Matrix(out_rep)
    ar=sp.zeros(3,1); ai=sp.zeros(3,1)
    for eps1 in (1,-1):
        p=sp.Matrix([eps1*x for x in r1])
        Ur,Ui=field(r1,s1,eps1)
        for eps2 in (1,-1):
            q=sp.Matrix([eps2*x for x in r2])
            if not same_vec(p+q,out):
                continue
            Vr,Vi=field(r2,s2,eps2)
            sr=Ur.dot(q); si=Ui.dot(q)
            # (sr+i si)(Vr+i Vi)
            ar += sr*Vr-si*Vi
            ai += sr*Vi+si*Vr
    # -i times the convolution
    wr,wi=ai,-ar
    k2=sp.expand(out.dot(out))
    pr=sp.simplify(wr-out*(out.dot(wr))/k2)
    pi=sp.simplify(wi-out*(out.dot(wi))/k2)
    e1,e2,n1,n2=basis(out_rep)
    ev=e1 if out_slot.startswith('e1') else e2
    norm=n1 if out_slot.startswith('e1') else n2
    re=sp.simplify(ev.dot(pr)/norm)
    im=sp.simplify(ev.dot(pi)/norm)
    return im if out_slot.endswith('im') else re


REPS=[(0,0,1),(n,-n,-1),(n,-n,0),(n,-n,0),(n,-n,1)]
SLOTS=['e1_re','e1_im','e1_re','e2_re','e1_im']


def h3_weights():
    out=[]
    for rep,slot in zip(REPS,SLOTS):
        e1,e2,n1,n2=basis(rep)
        physical=n1 if slot.startswith('e1') else n2
        k2=sp.expand(sp.Matrix(rep).dot(sp.Matrix(rep)))
        out.append(sp.factor(physical*(1+k2)**3))
    return out


def monomial_coefficient(mon,W):
    acc=0
    for i,j,k in set(itertools.permutations(mon)):
        acc += W[i]*bilinear_coordinate(REPS[i],SLOTS[i],REPS[j],SLOTS[j],REPS[k],SLOTS[k])
    return sp.factor(sp.simplify(acc))


def main():
    W=h3_weights()
    mons=((0,1,2),(0,1,3),(0,2,4),(0,3,4))
    got=[monomial_coefficient(mon,W) for mon in mons]
    A=sp.factor(n**3*(4*n**4-6*n**2-17))
    B=sp.factor(2*n**3*(4*n**6-6*n**2-7))
    expected=[A,-B,A,B]
    for g,e in zip(got,expected):
        assert sp.simplify(g-e)==0, (g,e)

    # Elementary non-vanishing proof obligations, encoded as exact endpoint/monotonic facts.
    fA=4*n**4-6*n**2-17
    fB=4*n**6-6*n**2-7
    assert sp.expand(fA.subs(n,1)) == -19
    assert sp.expand(fA.subs(n,2)) == 23
    assert sp.factor(sp.diff(fA,n)) == 4*n*(4*n**2-3)
    assert sp.expand(fB.subs(n,1)) == -9
    assert sp.expand(fB.subs(n,2)) == 225
    assert sp.factor(sp.diff(fB,n)) == 12*n*(2*n**4-1)
    # Derivatives are positive for real n>=1. Hence each factor is strictly increasing;
    # its only integer sign change is between n=1 and n=2, so no positive integer zero.

    product=sp.factor(expected[0]*expected[1]*expected[2]*expected[3])
    assert sp.simplify(product + A**2*B**2)==0

    print('NS P2 symbolic all-n ladder frustration')
    print('coefficients:', [sp.factor(v) for v in got])
    print('A_n =', A)
    print('B_n =', B)
    print('coefficient product = -A_n^2 B_n^2 < 0 for every integer n>=1')
    print('scope: parameterized ladder family only; boundary coverage remains OPEN')
    print('NS-P2 ALL-N LADDER FRUSTRATION PASS')


if __name__=='__main__':
    main()
