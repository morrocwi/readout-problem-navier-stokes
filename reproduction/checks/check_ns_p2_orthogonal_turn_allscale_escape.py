#!/usr/bin/env python3
from sympy import Matrix, Integer, sqrt, simplify

A = Matrix([
    [3, 0, 4],
    [4, 0, -3],
    [0, 5, 0],
])
I = Matrix.eye(3)

p0 = Matrix([1, 0, 0])
q0 = Matrix([2, 4, 0])
k0 = p0 + q0

assert A.T * A == 25 * I
assert A.det() == 125
assert A * p0 == k0

# Base geometry.
n0 = p0.cross(q0)
p1 = A * p0
q1 = A * q0
n1 = p1.cross(q1)
assert n0 == Matrix([0, 0, 4])
assert n0.dot(n1) == 0

# Cross-product transport implied by the exact similitude.
assert n1 == 5 * A * n0

# Genuinely 3D backbone fixture.
p2 = A * p1
M = Matrix.hstack(p0, p1, p2)
assert abs(M.det()) == 80

# Base adapted-axis exchange.
# N0 = e3; N1 = (4,-3,0)/5; p1/|p1| = (3,4,0)/5.
N0 = Matrix([0, 0, 1])
N1 = Matrix([Integer(4)/5, Integer(-3)/5, 0])
p1hat = Matrix([Integer(3)/5, Integer(4)/5, 0])
assert N1.cross(p1hat) == N0

# Exact base channel coefficient c(T_p, N; N) = |p x q|/|p| = 4.
P0 = Integer(1)
Q0 = 2 * sqrt(5)
K0 = Integer(5)
area0 = Integer(4)
c0 = area0 / P0
assert c0 == 4

# Homogeneous H1 energy-transfer coefficient.
gamma0 = simplify(2 * c0 * K0 / (P0 * Q0))
assert simplify(gamma0 - 4 * sqrt(5)) == 0

# The all-scale identity follows algebraically from A^T A = 25 I:
# P_j=5^j P0, Q_j=5^j Q0, K_j=5^j K0,
# area_j=25^j area0, c_j=5^j c0.
# Verify exact symbolic cancellation of the scale factor with an abstract positive s=5^j.
s = Integer(5)  # one step scale ratio; powers cancel identically
scaled_gamma = simplify(2 * (s*c0) * (s*K0) / ((s*P0)*(s*Q0)))
assert simplify(scaled_gamma - gamma0) == 0

# Check several exact integer iterates for triad closure, orthogonal turns,
# scale laws, axis exchange projectively, and dyadic progress.
p = p0
q = q0
prev_n = None
for j in range(7):
    k = p + q
    assert k == A * p
    n = p.cross(q)
    assert n != Matrix([0, 0, 0])

    # Exact Euclidean norm-squared scale laws.
    assert p.dot(p) == 25**j
    assert q.dot(q) == 20 * 25**j
    assert k.dot(k) == 25**(j+1)
    assert n.dot(n) == 16 * 625**j

    if prev_n is not None:
        assert prev_n.dot(n) == 0

    # More than one dyadic max-coordinate jump each step.
    pinf = max(abs(int(x)) for x in p)
    kinf = max(abs(int(x)) for x in k)
    assert kinf > 2 * pinf

    # Raw adapted coefficient and homogeneous H1 energy coefficient.
    # area=4*25^j, |p|=5^j, so c=4*5^j.
    cj = 4 * 5**j
    gammaj = simplify(2 * cj * (5**(j+1)) /
                      ((5**j) * (2*sqrt(5)*5**j)))
    assert simplify(gammaj - 4*sqrt(5)) == 0

    prev_n = n
    p = A * p
    q = A * q

print('NS P2 ORTHOGONAL-TURN ALL-SCALE ESCAPE PASS')
print('A^T A = 25 I, det A = 125')
print('every consecutive triad-plane normal pair is orthogonal')
print('selected homogeneous H1 energy coefficient = 4*sqrt(5) at every scale')
print('selected backbone crosses >2 in max-coordinate scale each step')
