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
s = Integer(5)
scaled_gamma = simplify(2 * (s*c0) * (s*K0) / ((s*P0)*(s*Q0)))
assert simplify(scaled_gamma - gamma0) == 0

# Check exact integer iterates for triad closure, orthogonal turns,
# scale laws, projective axis exchange, and dyadic progress.
p = p0
q = q0
prev_n = None
for j in range(9):
    k = p + q
    assert k == A * p
    n = p.cross(q)
    assert n != Matrix([0, 0, 0])

    assert p.dot(p) == 25**j
    assert q.dot(q) == 20 * 25**j
    assert k.dot(k) == 25**(j+1)
    assert n.dot(n) == 16 * 625**j

    if prev_n is not None:
        assert prev_n.dot(n) == 0
        # For triad j, T_j is projectively n_j x p_j.
        # Orthogonal-turn geometry makes it parallel to N_{j-1},
        # so the previous output polarization is the next input polarization.
        tangent = n.cross(p)
        assert tangent.cross(prev_n) == Matrix([0, 0, 0])
        assert tangent.dot(prev_n) != 0

    pinf = max(abs(int(x)) for x in p)
    kinf = max(abs(int(x)) for x in k)
    assert kinf > 2 * pinf

    cj = 4 * 5**j
    gammaj = simplify(2 * cj * (5**(j+1)) /
                      ((5**j) * (2*sqrt(5)*5**j)))
    assert simplify(gammaj - 4*sqrt(5)) == 0

    prev_n = n
    p = A * p
    q = A * q

# Exact finite-prefix phase-SAT fixture in quarter-turn units Z/4Z.
# With the chosen oriented adapted coefficient positive, use the target
# phi(P_j)+phi(Q_j)-phi(P_{j+1}) = 1 mod 4.
# Setting every backbone phase to 0 and every fresh donor phase to 1
# satisfies every selected-channel constraint simultaneously.
for J in (1, 2, 4, 8, 16, 32):
    phi_p = [0] * (J + 1)
    phi_q = [1] * J
    for j in range(J):
        assert (phi_p[j] + phi_q[j] - phi_p[j+1]) % 4 == 1

print('NS P2 ORTHOGONAL-TURN ALL-SCALE ESCAPE PASS')
print('A^T A = 25 I, det A = 125')
print('every consecutive triad-plane normal pair is orthogonal')
print('projective output/input adapted axes chain exactly')
print('selected homogeneous H1 energy coefficient = 4*sqrt(5) at every scale')
print('selected finite prefixes are phase-SAT in Z/4Z')
print('selected backbone crosses >2 in max-coordinate scale each step')
