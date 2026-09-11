#!/usr/bin/env python3
"""Exact polarization-gauge red-team and shared-frame identities for P2."""
import itertools
import sympy as sp

P, x, y = sp.symbols("P x y", positive=True, real=True)
c, s = sp.symbols("c s", real=True, nonzero=True)
Q2 = x**2 + y**2
K2 = P**2 + 2*P*x + x**2 + y**2
Q = sp.sqrt(Q2)
K = sp.sqrt(K2)

p = sp.Matrix((P, 0, 0))
q = sp.Matrix((x, y, 0))
N = sp.Matrix((0, 0, 1))
Tp = sp.Matrix((0, 1, 0))
Tq = sp.Matrix((-y/Q, x/Q, 0))
Tk = sp.Matrix((-y/K, (P+x)/K, 0))


def coupling(hp, hq, hk):
    return sp.factor(sp.simplify(hp.dot(q)*hk.dot(hq) + hq.dot(p)*hk.dot(hp)))

P_SLOTS = (N, Tp)
Q_SLOTS = (N, Tq)
K_SLOTS = (N, Tk)
TENSOR = {
    (i,j,l): coupling(P_SLOTS[i], Q_SLOTS[j], K_SLOTS[l])
    for i,j,l in itertools.product(range(2), repeat=3)
}

# Seven entries compare directly.  For the tangent-tangent-tangent entry we
# verify the radical-free squared identity plus its sign factor; this avoids a
# purely syntactic SymPy distinction between equivalent expanded radicals.
EXPECTED_DIRECT = {
    (0,0,0): 0,
    (0,0,1): 0,
    (0,1,0): -P*y/Q,
    (0,1,1): 0,
    (1,0,0): y,
    (1,0,1): 0,
    (1,1,0): 0,
}

E1 = c*N + s*Tp
E2 = -s*N + c*Tp
ROTATED_FACE = (
    coupling(E1,Tq,N), coupling(E1,N,N),
    coupling(E2,Tq,N), coupling(E2,N,N),
)
ROTATED_FACE_PRODUCT = sp.factor(sp.prod(ROTATED_FACE))
EXPECTED_FACE_PRODUCT = -P**2*y**4*c**2*s**2/Q2

# Old coplanar all-n ladder: exact adapted-frame SAT witness in quarter turns.
LADDER_EQUATIONS=[]
def add_eq(terms,target):
    row=[0]*8
    for idx,coef in terms: row[idx]+=coef
    LADDER_EQUATIONS.append((tuple(row),target%4))
add_eq(((0,1),(3,1),(4,-1)),-1)
add_eq(((1,1),(2,1),(4,-1)),+1)
add_eq(((1,1),(3,1),(5,-1)),+1)
add_eq(((0,1),(5,1),(6,-1)),-1)
add_eq(((1,1),(4,1),(6,-1)),+1)
add_eq(((1,1),(5,1),(7,-1)),+1)
LADDER_SAT_ASSIGNMENT=(0,0,0,2,3,1,2,0)

# Explicit all-n noncoplanar shared-mode pair with projective delta=pi/4.
n=sp.symbols("n", positive=True, integer=True)
p0=sp.Matrix((0,0,n)); q1=sp.Matrix((n,0,0)); q2=sp.Matrix((n,n,0))
n1=p0.cross(q1); n2=p0.cross(q2)
cos_alpha=sp.simplify(n1.dot(n2)/sp.sqrt(n1.dot(n1)*n2.dot(n2)))
SIN_PI_8=sp.sqrt(2-sp.sqrt(2))/2
RAW_FACE_FLOOR=sp.simplify(n*SIN_PI_8)
G1=sp.simplify(4*sp.sqrt(2)*SIN_PI_8/n**2)
G2=sp.simplify(sp.Rational(3,2)*sp.sqrt(6)*SIN_PI_8/n**2)
G_HOM=G2
G_INH=sp.simplify(G_HOM/8)

# Exact weighted projective-frame dispersion fixture.
W=sp.Integer(6)
Z_RE=sp.Rational(-2,6); Z_IM=sp.Rational(2,6)
D=sp.simplify(1-Z_RE**2-Z_IM**2)
PAIR_SUM=sp.simplify(1*2*sp.Rational(1,2)+1*3+2*3*sp.Rational(1,2))
D_PAIRS=sp.simplify(4*PAIR_SUM/W**2)
a0=sp.Rational(1,4)
PAIR_TOTAL=sp.Integer(11)
PAIR_LOWER=sp.simplify(W**2*(D/4-a0/2)/(1-a0))


def main():
    for idx,e in EXPECTED_DIRECT.items():
        assert sp.simplify(TENSOR[idx]-e)==0, (idx,TENSOR[idx],e)

    g=sp.factor(TENSOR[(1,1,1)])
    target_num=y*(Q2-P**2)
    # g = target_num/(sqrt(Q2)*sqrt(K2)); verify without radical rewriting.
    assert sp.simplify(g**2*Q2*K2-target_num**2)==0
    assert sp.simplify(g*Q*K-target_num)==0

    nonzero=[idx for idx,val in TENSOR.items() if sp.simplify(val)!=0]
    assert nonzero==[(0,1,0),(1,0,0),(1,1,1)]
    assert sp.simplify(ROTATED_FACE_PRODUCT-EXPECTED_FACE_PRODUCT)==0

    for row,target in LADDER_EQUATIONS:
        lhs=sum(row[i]*LADDER_SAT_ASSIGNMENT[i] for i in range(8))%4
        assert lhs==target

    assert cos_alpha==sp.sqrt(2)/2
    assert sp.N(G1-G_HOM)>0
    assert sp.simplify(G_INH-sp.Rational(3,16)*sp.sqrt(6)*SIN_PI_8/n**2)==0

    assert D==sp.Rational(7,9)
    assert D_PAIRS==D
    assert PAIR_SUM==7
    assert PAIR_LOWER==sp.Rational(10,3)
    assert PAIR_TOTAL>=PAIR_LOWER

    print("NS P2 polarization gauge / frame mismatch checker")
    print("adapted triad nonzero tensor entries:", [(i,sp.factor(TENSOR[i])) for i in nonzero])
    print("rotated-face product:", ROTATED_FACE_PRODUCT)
    print("old coplanar ladder adapted-frame SAT assignment:", LADDER_SAT_ASSIGNMENT)
    print("explicit pair frame cos(alpha):", cos_alpha)
    print("raw face floor:", RAW_FACE_FLOOR)
    print("homogeneous H3 uniform floor:", G_HOM)
    print("inhomogeneous H3 uniform floor:", G_INH)
    print("weighted frame dispersion fixture:", D)
    print("scope: gauge geometry only; global transfer coverage remains OPEN")
    print("NS-P2 POLARIZATION GAUGE FRAME CHECK PASS")

if __name__=="__main__":
    main()
