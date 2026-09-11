#!/usr/bin/env python3
"""Exact H1-normalized coefficient floor for the gauge-compatible dyadic cycle.

This uses the same all-n network and global compatible frame as
check_ns_p2_frame_compatible_dyadic_holonomy.py, but normalizes scalar
coordinates with homogeneous H1 weights.  The four-channel holonomy cycle has
a cutoff-uniform homogeneous H1 coefficient floor sqrt(2), and the standard
integer-mode comparison gives a conservative inhomogeneous H1 floor
sqrt(2)/2.  This normalization is the one aligned with the finite-observation
quantity K_N in the P2B scale-contraction route.
"""
import sympy as sp

n = sp.symbols("n", positive=True, integer=True)
V = {
    "p": sp.Matrix((n,0,n)),
    "c": sp.Matrix((0,n,0)),
    "q": sp.Matrix((n,n,n)),
    "k": sp.Matrix((2*n,n,2*n)),
}
y = sp.Matrix((0,1,0))
d = sp.Matrix((-1,0,1))
H = {
    "p": (y,d),
    "c": (d,sp.Matrix((-1,0,-1))),
    "q": (d,sp.Matrix((-1,2,-1))),
    "k": (d,sp.Matrix((-1,4,-1))),
}


def coupling(m1,s1,m2,s2,out,so):
    v1,v2,vo=V[m1],V[m2],V[out]
    assert v1+v2==vo
    h1,h2,ho=H[m1][s1],H[m2][s2],H[out][so]
    return sp.factor((h1.dot(v2)*ho.dot(h2)+h2.dot(v1)*ho.dot(h1))/ho.dot(ho))


def h1_hom_weight(mode,slot):
    v=V[mode]; h=H[mode][slot]
    return sp.factor(h.dot(h)*v.dot(v))


def gamma_h1(ch):
    m1,s1,m2,s2,out,so=ch
    cc=coupling(*ch)
    return sp.factor(
        2*cc*sp.sqrt(h1_hom_weight(out,so))
        /sp.sqrt(h1_hom_weight(m1,s1)*h1_hom_weight(m2,s2))
    )

CYCLE = {
    "T1B": ("p",0,"c",1,"q",1),
    "T1C": ("p",1,"c",1,"q",0),
    "T2A": ("p",0,"q",0,"k",0),
    "T2C": ("p",1,"q",1,"k",0),
}
EXPECTED = {
    "T1B": -sp.sqrt(2),
    "T1C": -2*sp.sqrt(3),
    "T2A": sp.sqrt(6),
    "T2C": -2,
}


def main():
    got={name:sp.simplify(gamma_h1(ch)) for name,ch in CYCLE.items()}
    for name in CYCLE:
        assert sp.simplify(got[name]-EXPECTED[name])==0, (name,got[name])

    floor_hom=sp.sqrt(2)
    for val in got.values():
        assert sp.N(abs(val)-floor_hom)>=0

    # For nonzero integer |ell|>=1,
    # R1(L)=sqrt(1+L^2)/L lies in [1,sqrt(2)].  Hence
    # Gamma_inh/Gamma_hom = R1(k)/(R1(p)R1(q)) >= 1/2.
    floor_inh=sp.simplify(floor_hom/2)
    assert floor_inh==sp.sqrt(2)/2

    print("NS P2 frame-compatible dyadic H1 floor")
    print("cycle homogeneous H1 coefficients:", got)
    print("cutoff-uniform homogeneous floor:", floor_hom)
    print("conservative inhomogeneous H1 floor:", floor_inh)
    print("alignment: H1 normalization matches the K_N finite-observation route")
    print("scope: local cycle floor; actual-flux coverage/time recurrence remain OPEN")
    print("NS-P2 FRAME-COMPATIBLE DYADIC H1 FLOOR PASS")

if __name__=="__main__":
    main()
