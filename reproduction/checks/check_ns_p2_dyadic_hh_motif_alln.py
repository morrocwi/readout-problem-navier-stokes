#!/usr/bin/env python3
"""Symbolic all-n dyadic high-high H3 frustration motif.

Take the homothetic triad
  q=(n,n,0), r=(n,-n,0), t=(2n,0,0), q+r=t,
with n a positive integer.  In the repository's divergence-free basis use
  z_q = a+i b on q/e1,
  z_r = c+i d on r/e2,
  z_t = e+i f on t/e1.

Direct symbolic Fourier convolution + Leray projection gives the H3 nonlinear
production subpolynomial

  Q_n = C_n(-a c f + a d e + b c e + b d f)
      = C_n Im(z_q z_r conjugate(z_t)),

  C_n = 8 n^7 (28 n^4 + 18 n^2 + 3) > 0.

Thus the four real monomials have an unavoidable sign-frustration for every n and,
crucially, this motif directly links max-frequency scale n to scale 2n.

After normalizing the three complex amplitudes by their inhomogeneous H3 modal
weights Wq,Wr,Wt, the trilinear coefficient Gamma_n obeys

  Gamma_n <= (7 sqrt(2))/(8 n^2).

The proof is an exact polynomial inequality.  This is a local high-high motif bound,
not a sum over the full triad network and not yet a global contraction theorem.
"""
import itertools
import sympy as sp

n=sp.symbols('n', positive=True, integer=True)


def basis(k):
    kv=sp.Matrix(k)
    for axis in (sp.Matrix((1,0,0)),sp.Matrix((0,1,0)),sp.Matrix((0,0,1))):
        e1=kv.cross(axis)
        if any(sp.simplify(v)!=0 for v in e1):
            e2=kv.cross(e1)
            return e1,e2,sp.expand(e1.dot(e1)),sp.expand(e2.dot(e2))
    raise AssertionError('zero wavevector not allowed')


def field(rep,slot,sgn):
    e1,e2,_,_=basis(rep)
    v=e1 if slot.startswith('e1') else e2
    if slot.endswith('im'):
        return sp.zeros(3,1),sgn*v
    return v,sp.zeros(3,1)


def same(a,b):
    return all(sp.simplify(a[i]-b[i])==0 for i in range(3))


def bcoord(out_rep,out_slot,r1,s1,r2,s2):
    out=sp.Matrix(out_rep)
    ar=sp.zeros(3,1); ai=sp.zeros(3,1)
    for eps1 in (1,-1):
        p=sp.Matrix([eps1*x for x in r1]); Ur,Ui=field(r1,s1,eps1)
        for eps2 in (1,-1):
            qv=sp.Matrix([eps2*x for x in r2])
            if not same(p+qv,out):
                continue
            Vr,Vi=field(r2,s2,eps2)
            sr=Ur.dot(qv); si=Ui.dot(qv)
            ar += sr*Vr-si*Vi
            ai += sr*Vi+si*Vr
    # -i times convolution, then Leray projection.
    wr,wi=ai,-ar
    k2=sp.expand(out.dot(out))
    pr=sp.simplify(wr-out*(out.dot(wr))/k2)
    pi=sp.simplify(wi-out*(out.dot(wi))/k2)
    e1,e2,n1,n2=basis(out_rep)
    ev=e1 if out_slot.startswith('e1') else e2
    norm=n1 if out_slot.startswith('e1') else n2
    re=sp.simplify(ev.dot(pr)/norm); im=sp.simplify(ev.dot(pi)/norm)
    return im if out_slot.endswith('im') else re


q=(n,n,0); r=(n,-n,0); t=(2*n,0,0)
REPS=[q,q,r,r,t,t]
SLOTS=['e1_re','e1_im','e2_re','e2_im','e1_re','e1_im']


def weights():
    out=[]
    for rep,slot in zip(REPS,SLOTS):
        e1,e2,n1,n2=basis(rep)
        physical=n1 if slot.startswith('e1') else n2
        k2=sp.expand(sp.Matrix(rep).dot(sp.Matrix(rep)))
        out.append(sp.factor(physical*(1+k2)**3))
    return out


def moncoeff(mon,W):
    acc=0
    for i,j,k in set(itertools.permutations(mon)):
        acc += W[i]*bcoord(REPS[i],SLOTS[i],REPS[j],SLOTS[j],REPS[k],SLOTS[k])
    return sp.factor(sp.simplify(acc))


def main():
    W=weights()
    mons=((0,2,5),(0,3,4),(1,2,4),(1,3,5))
    got=[moncoeff(m,W) for m in mons]
    C=sp.factor(8*n**7*(28*n**4+18*n**2+3))
    expected=[-C,C,C,C]
    for g,e in zip(got,expected):
        assert sp.simplify(g-e)==0,(g,e)

    # H3 weights of each complex coordinate pair.
    Wq=sp.factor(n**2*(1+2*n**2)**3)
    Wr=sp.factor(2*n**4*(1+2*n**2)**3)
    Wt=sp.factor(4*n**2*(1+4*n**2)**3)
    assert sp.simplify(W[0]-Wq)==0 and sp.simplify(W[1]-Wq)==0
    assert sp.simplify(W[2]-Wr)==0 and sp.simplify(W[3]-Wr)==0
    assert sp.simplify(W[4]-Wt)==0 and sp.simplify(W[5]-Wt)==0

    Gamma=sp.factor(C/sp.sqrt(Wq*Wr*Wt))
    target=sp.Rational(7,8)*sp.sqrt(2)/n**2

    # Prove Gamma <= target by squaring positive quantities and exposing a
    # polynomial with strictly positive coefficients in x=n^2.
    x=sp.symbols('x', positive=True)
    den=(2*x+1)**6*(4*x+1)**3
    lhs_num=8*x**5*(28*x**2+18*x+3)**2  # (n^2 Gamma)^2 numerator
    difference=sp.factor(sp.Rational(49,32)*den-lhs_num)
    expected_positive=(
        494592*x**8 + 1115904*x**7 + 1154624*x**6 + 712704*x**5
        + 284592*x**4 + 74480*x**3 + 12348*x**2 + 1176*x + 49
    )/32
    assert sp.simplify(difference-expected_positive)==0
    assert all(c>0 for c in sp.Poly(sp.together(difference),x).all_coeffs())

    print('NS P2 symbolic dyadic high-high motif')
    print('H3 cubic coefficients:', got)
    print('C_n =', C)
    print('Q_n/C_n = -acf + ade + bce + bdf = Im(z_q z_r conjugate(z_t))')
    print('Gamma_n =', Gamma)
    print('exact bound: Gamma_n <= 7*sqrt(2)/(8*n^2)')
    print('scale link: q,r have max norm n; t has max norm 2n')
    print('scope: one homothetic HH motif family; full-network coverage/sum remains OPEN')
    print('NS-P2 DYADIC HH MOTIF ALL-N PASS')


if __name__=='__main__':
    main()
