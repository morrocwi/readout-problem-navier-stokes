#!/usr/bin/env python3
"""Exact checker for PROP-P3-FORCED-ADDRESS-ACCOUNTING-01 and
PROP-P3-RSC-O-SKELETON-FIXTURES-01.

Forced-address accounting completeness (the rule, as a checker obligation):
  in an exact closure question, every registered address that receives nonzero
  individual forcing must be explicitly represented and resolved with one outcome
  from {ACTIVE (amplitude != 0), EXACT-CANCELLED (net forcing 0, individual
  contributions != 0, ledgered), NULL-BY-REGISTERED-GEOMETRY (ORTH / EQSHELL
  nullity), TED (outside the declared cell)}.  A forced address absent from the
  state / ledger is UNRESOLVED and the closure test is INVALID.

Encoded per forced address as the exact disjunction

      (amplitude != 0)  or  (net forcing into the address == 0),

run as two exact polynomial systems (reduced grevlex Groebner bases over QQ,
Rabinowitsch saturation for every "!= 0"):

  System A : amplitude saturated nonzero               (ACTIVE branch)
  System B : amplitude == 0  and  net forcing == 0     (EXACT-CANCELLED or
                                                        NULL-BY-GEOMETRY branch)
  Forgotten: amplitude == 0  and  net forcing != 0     (the loophole; a SAT here
                                                        is a spurious closure point)

Fixtures (one fixed skeleton, m <= 3, finite_diagnostic):
  skeleton  p+ = (1,0,0), a+ = (0,1,0), p- = (0,1,0), a- = (0,0,1),
            core k = p+ + p- = (1,1,0) with free polarization c = (c1,-c1,c3) in k^perp;
  F1  single-O alternation, double-O excluded, m = 2, 3;
  F2  one-sided O_+ recruit layer + active O_- core, m = 1, 2;
  F3  A3 shell-9 identity-monodromy rectangle +-{(2,-2,+-1),(-2,-2,+-1)}: no pair
      sum lands on its own addresses (NO_INSIDE_TARGET).

Bilinear form: B(p,q,a,b) = P_{p+q}[(a.q) b + (b.p) a] with the DENOMINATOR-CLEARED
projection P_k[v] = (k.k) v - (v.k) k.  Over the reals this has the same zero set as
the Leray projection for k != 0; over the complex variety that a QQ Groebner basis
certifies, an isotropic k (k.k = 0, k != 0) degenerates it to the rank-one map
v -> -(v.k) k whose kernel k^perp contains k, so the outside-zero equation becomes far
weaker than Leray's.  Every symbolic pair-sum t is therefore saturated by t.t != 0 in
every system below (this also removes the real antipodal sums t = 0), and
the checker records separately that WITHOUT that saturation the single-O fixture
admits complex isotropic points (q = (0,0,+-i)) that are not real witnesses.

This checker proves nothing about RSC-O globally, OCSR, Witness Soundness, G6/G7 or
Clay Navier-Stokes regularity.  All arithmetic is exact (sympy); no floats.
"""

import itertools
import sys
import time

import sympy as sp
from sympy import groebner

T0 = time.time()


def proj(v, k):
    return (k.dot(k)) * v - (v.dot(k)) * k


def B(p, q, a, b):
    return proj((a.dot(q)) * b + (b.dot(p)) * a, p + q)


def V(*xs):
    return sp.Matrix([sp.nsimplify(x) for x in xs])


def is_unsat(G):
    return list(G.exprs) == [1]


def gb(polys, gens):
    polys = [sp.expand(e) for e in polys]
    polys = [e for e in polys if e != 0]
    return groebner(polys, *gens, order='grevlex', domain=sp.QQ)


# ---------------------------------------------------------------------------
# Skeleton
# ---------------------------------------------------------------------------
PP, AP = V(1, 0, 0), V(0, 1, 0)      # O_+ anchor
PM, AM = V(0, 1, 0), V(0, 0, 1)      # O_- anchor
KK = PP + PM                         # core address k = (1,1,0)
c1, c3 = sp.symbols('c1 c3')
CK = sp.Matrix([c1, -c1, c3])        # free polarization in k^perp
assert CK.dot(KK) == 0
assert AP.dot(PP) == 0 and AM.dot(PM) == 0

# anchor-anchor forcing into k: the only numeric contribution to F(k)
F_K_ANCHOR = B(PP, PM, AP, AM).applyfunc(sp.expand)
assert F_K_ANCHOR == V(0, 0, 2), F_K_ANCHOR

# System A is refuted at m = 0: the anchor-core pairs force the outside targets (2,1,0) and
# (1,2,0); their outside-zero equations alone reduce to c1 = c3 = 0.
_G0 = groebner([sp.expand(x) for x in list(B(PP, KK, AP, CK)) + list(B(PM, KK, AM, CK)) if sp.expand(x) != 0],
               c1, c3, order='grevlex', domain=sp.QQ)
assert set(_G0.exprs) == {c1, c3}, list(_G0.exprs)
assert tuple(PP + KK) == (2, 1, 0) and tuple(PM + KK) == (1, 2, 0)


def skeleton_web(kind, m):
    """Return (Q, Bv, eqs, sat, gens) for the recruit family of a fixture."""
    z = sp.symbols(f'z0:{m}')
    w = sp.symbols(f'w0:{m}')
    eqs, sat = [], []
    if kind == 'single':
        Q = [sp.Matrix(sp.symbols(f'q{j}_0:3')) for j in range(m)]
        Bv = [sp.Matrix(sp.symbols(f'b{j}_0:3')) for j in range(m)]
        anchors = {'+': (PP, AP), '-': (PM, AM)}
        for j in range(m):
            s = '+' if j % 2 == 0 else '-'
            t = '-' if s == '+' else '+'
            ps, as_ = anchors[s]
            _, at = anchors[t]
            eqs.append(as_.dot(Q[j]))                   # genuine single-O on anchor s
            sat.append(z[j] * at.dot(Q[j]) - 1)         # double-O excluded
            eqs.append(Bv[j].dot(Q[j]))                 # divergence-free recruit
            sat.append(w[j] * Bv[j].dot(Bv[j]) - 1)     # recruit amplitude nonzero
            eqs += list(B(ps, Q[j], as_, Bv[j]))        # suppression of the s-anchor interaction
        gens = [x for q in Q for x in q] + [x for b in Bv for x in b]
    elif kind == 'onesided':
        X = sp.symbols(f'x0:{m}')
        Y = sp.symbols(f'yy0:{m}')
        S = sp.symbols(f's0:{m}')
        Q = [sp.Matrix([X[j], 0, Y[j]]) for j in range(m)]     # q_j in a_+^perp
        Bv = [S[j] * AP for j in range(m)]                    # [b_j] = [a_+]  (ALT-1)
        for j in range(m):
            sat.append(z[j] * AM.dot(Q[j]) - 1)               # genuine single-O: a_-.q_j != 0
            sat.append(w[j] * S[j] - 1)                       # recruit amplitude nonzero
            assert B(PP, Q[j], AP, Bv[j]).applyfunc(sp.expand) == sp.zeros(3, 1)
        gens = list(X) + list(Y) + list(S)
    else:
        raise ValueError(kind)
    gens += list(z) + list(w)
    return Q, Bv, eqs, sat, gens


def closure_systems(kind, m):
    """Build the outside-closure equations, productivity, isotropy saturations and the
    net forcing into k for one fixture.  Returns a dict of exact Groebner verdicts."""
    Q, Bv, eqs, sat, gens = skeleton_web(kind, m)
    eqs_recruit = list(eqs)          # recruit-only constraints (no core polarization)
    web = [(PP, AP), (PM, AM), (KK, CK)] + list(zip(Q, Bv))
    inside_numeric = [tuple(PP), tuple(PM), tuple(KK)]

    targets = {}
    for (p1, a1), (p2, a2) in itertools.combinations(web, 2):
        t = p1 + p2
        targets.setdefault(tuple(t), []).append(B(p1, p2, a1, a2))

    prod = sp.Integer(0)
    iso = []
    f_k = sp.zeros(3, 1)
    for t, fs in targets.items():
        net = sum(fs, sp.zeros(3, 1))
        tv = sp.Matrix(t)
        numeric = all(x.is_number for x in t)
        if numeric and tuple(tv) in inside_numeric:
            prod += net.dot(net)
            if tuple(tv) == tuple(KK):
                f_k = f_k + net
        else:
            # every other target (numeric-outside or symbolic) must carry zero net forcing
            eqs += list(net)
            if not numeric:
                iso.append(tv.dot(tv))
    assert prod != 0, 'ansatz has no inside target'
    assert f_k.applyfunc(sp.expand) == F_K_ANCHOR, f_k

    u = sp.symbols('u')
    ys = sp.symbols(f'iso0:{len(iso)}')
    base = list(eqs)
    base_sat = list(sat) + [u * prod - 1]
    iso_sat = [y * e - 1 for y, e in zip(ys, iso)]
    base_gens = list(gens) + [u, c1, c3] + list(ys)

    out = {}
    vpop = sp.symbols('vpop')

    # System A : core amplitude saturated nonzero (ACTIVE)
    GA = gb(base + base_sat + iso_sat + [vpop * (c1**2 + c3**2) - 1], base_gens + [vpop])
    out['A'] = 'UNSAT' if is_unsat(GA) else f'SAT({len(GA.exprs)})'

    # System B : core amplitude zero AND net forcing into k zero
    GB_ = gb(base + base_sat + iso_sat + [c1, c3] + list(f_k), base_gens)
    out['B'] = 'UNSAT' if is_unsat(GB_) else f'SAT({len(GB_.exprs)})'

    # Forgotten case : core amplitude zero AND net forcing into k nonzero (the loophole)
    vf = sp.symbols('vforce')
    GF = gb(base + base_sat + iso_sat + [c1, c3, vf * f_k.dot(f_k) - 1], base_gens + [vf])
    out['forgotten'] = 'UNSAT' if is_unsat(GF) else f'SAT({len(GF.exprs)})'
    out['forgotten_gb'] = GF

    # Same forgotten case WITHOUT the isotropy saturation (what the raw source runs certify)
    GF0 = gb(base + base_sat + [c1, c3, vf * f_k.dot(f_k) - 1], list(gens) + [u, c1, c3, vf])
    out['forgotten_no_iso'] = 'UNSAT' if is_unsat(GF0) else f'SAT({len(GF0.exprs)})'
    out['forgotten_no_iso_gb'] = GF0

    # Coincidence audit for F(k).  A recruit sum can land on k only as
    #   (i)  q_i + q_j = k          -> checked exactly: UNSAT under the recruit constraints;
    #   (ii) q_j + p_{+-} = k        <=> q_j = p_{-+} identically (linear): the "recruit" would sit
    #                                  on an anchor address, i.e. modify the FIXED skeleton; a recruit
    #                                  is by definition a new registered address, so (ii) is excluded.
    # Hence F(k) = anchor-anchor forcing = (0,0,2) on the admissible set.
    out['coincidence'] = {}
    for i, j in itertools.combinations(range(m), 2):
        Gc = gb(eqs_recruit + list(sat) + list(Q[i] + Q[j] - KK), list(gens))
        out['coincidence']['q%d+q%d=k' % (i, j)] = 'UNSAT' if is_unsat(Gc) else 'SAT'
    for j in range(m):
        assert (Q[j] + PP - KK) == (Q[j] - PM)
        assert (Q[j] + PM - KK) == (Q[j] - PP)
    out['Q'] = Q
    out['Bv'] = Bv
    out['gens'] = gens
    out['eqs'] = eqs
    out['sat'] = sat
    out['prod'] = prod
    out['iso'] = iso
    return out


def verify_point(kind, m, res, point):
    """Re-verify an explicit point by exact substitution: all outside forcing zero,
    all recruit constraints hold, all saturated quantities nonzero, core forced but empty."""
    subs = dict(point)
    subs[c1] = 0
    subs[c3] = 0
    for e in res['eqs']:
        val = sp.expand(sp.sympify(e).subs(subs))
        assert val == 0, (e, val)
    # saturations: the polynomial with the auxiliary variable removed must be nonzero
    for s in res['sat']:
        s = sp.sympify(s)
        aux = [g for g in s.free_symbols if str(g).startswith(('z', 'w'))]
        assert len(aux) == 1, s
        core = sp.expand((s + 1).subs(aux[0], 1).subs(subs))   # s = aux*X - 1 -> X
        assert core != 0, (s, core)
    for e in res['iso']:
        assert sp.expand(sp.sympify(e).subs(subs)) != 0, e
    assert sp.expand(sp.sympify(res['prod']).subs(subs)) != 0
    return True


# ---------------------------------------------------------------------------
# F3: A3 shell-9 identity-monodromy rectangle — NO_INSIDE_TARGET
# ---------------------------------------------------------------------------
def rectangle_no_inside_target():
    S = [(2, -2, 1), (2, -2, -1), (-2, -2, 1), (-2, -2, -1)]
    S = S + [tuple(-x for x in v) for v in S]
    assert len(set(S)) == 8
    assert all(v[0]**2 + v[1]**2 + v[2]**2 == 9 for v in S)
    Sset = set(S)
    inside, outside = 0, 0
    for p, q in itertools.combinations(S, 2):
        t = tuple(a + b for a, b in zip(p, q))
        if t == (0, 0, 0):
            continue
        if t in Sset:
            inside += 1
        else:
            outside += 1
    assert inside == 0, inside
    assert outside == 24, outside            # 24 ordered-unordered pairs excluding the 4 antipodal ones
    # distinct outside targets: 18 (as the source run recorded)
    tg = {tuple(a + b for a, b in zip(p, q)) for p, q in itertools.combinations(S, 2)}
    tg.discard((0, 0, 0))
    assert len(tg) == 18, len(tg)
    return 'NO_INSIDE_TARGET'


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
def main():
    print('NS P2 forced-address accounting checker (exact, sympy/QQ)')
    print('skeleton p+=(1,0,0) a+=(0,1,0) p-=(0,1,0) a-=(0,0,1) core k=(1,1,0) c=(c1,-c1,c3)')
    print('anchor-anchor forcing into k =', tuple(F_K_ANCHOR), '(nonzero, independent of every recruit)')
    print('System A refuted at m = 0: anchor-core exits (2,1,0), (1,2,0) give Groebner basis [c1, c3]; '
          'A/B UNSAT columns below are skeleton-level, the forgotten column is recruit-dependent')

    # F3
    r3 = rectangle_no_inside_target()
    print(f'F3 A3 shell-9 rectangle: {r3} (8 addresses, 18 distinct outside targets, 0 inside)')
    assert r3 == 'NO_INSIDE_TARGET'

    expected = {
        ('single', 2):   dict(A='UNSAT', B='UNSAT', forgotten='UNSAT', forgotten_no_iso='SAT'),
        ('single', 3):   dict(A='UNSAT', B='UNSAT', forgotten='UNSAT', forgotten_no_iso='SAT'),
        ('onesided', 1): dict(A='UNSAT', B='UNSAT', forgotten='SAT',   forgotten_no_iso='SAT'),
        ('onesided', 2): dict(A='UNSAT', B='UNSAT', forgotten='SAT',   forgotten_no_iso='SAT'),
    }
    results = {}
    for (kind, m), exp in expected.items():
        t0 = time.time()
        res = closure_systems(kind, m)
        dt = time.time() - t0
        results[(kind, m)] = res
        label = 'F1 single-O alternation' if kind == 'single' else 'F2 one-sided O+ layer + O- core'
        print(f'{label} m={m}: System A (core ACTIVE) {res["A"]} | System B (core empty, F(k)=0) {res["B"]} | '
              f'forgotten (core empty, F(k)!=0) {res["forgotten"]} | forgotten without isotropy saturation '
              f'{res["forgotten_no_iso"]} | coincidences {res["coincidence"]} | {dt:.1f}s')
        for key in ('A', 'B', 'forgotten', 'forgotten_no_iso'):
            assert res[key].startswith(exp[key]), (kind, m, key, res[key])
        assert all(v == 'UNSAT' for v in res['coincidence'].values()), res['coincidence']

    # System B is refuted by a constant: F(k) = (0,0,2) whatever the recruits do (coincidences excluded)
    assert F_K_ANCHOR.dot(F_K_ANCHOR) == 4

    # F1: the raw (no isotropy saturation) single-O "points" are complex isotropic artifacts:
    # the reduced basis contains z0**2 + 1 and q0_2 + z0, so q0 = (0,0,+-i) and (p+ + q0).(p+ + q0) = 0.
    for m in (2, 3):
        G0 = results[('single', m)]['forgotten_no_iso_gb']
        z0 = sp.symbols('z0')
        q0_2 = sp.symbols('q0_2')
        exprs = set(G0.exprs)
        assert (z0**2 + 1) in exprs, 'isotropic artifact marker missing'
        assert (q0_2 + z0) in exprs, 'isotropic artifact marker missing'
        k_iso = PP + sp.Matrix([0, 0, sp.I])
        assert sp.expand(k_iso.dot(k_iso)) == 0
    print('F1 raw single-O points: q0 = (0,0,+-i), k = p+ + q0 isotropic (k.k = 0) -> not real witnesses; '
          'with t.t != 0 saturated the unpopulated single-O system is UNSAT for m = 2, 3')

    # F2: explicit REAL rational witness for the forgotten case, m = 1: q0 = (0,0,1), b0 = a+, c = 0
    res1 = results[('onesided', 1)]
    x0, yy0, s0 = sp.symbols('x0 yy0 s0')
    for sign in (1, -1):
        point = {x0: 0, yy0: sign, s0: 1}
        assert verify_point('onesided', 1, res1, point)
        # explicit forcing check at the point
        q0 = V(0, 0, sign)
        b0 = AP
        assert AP.dot(q0) == 0 and AM.dot(q0) == sign
        assert B(PP, q0, AP, b0).applyfunc(sp.expand) == sp.zeros(3, 1)     # O_+ silent
        # every target outside {p+, p-, k} vanishes at c = 0
        web = [(PP, AP), (PM, AM), (KK, sp.zeros(3, 1)), (q0, b0)]
        for (p1, a1), (p2, a2) in itertools.combinations(web, 2):
            t = p1 + p2
            f = B(p1, p2, a1, a2).applyfunc(sp.expand)
            if tuple(t) in {tuple(PP), tuple(PM), tuple(KK)}:
                continue
            assert f == sp.zeros(3, 1), (t, f)
        # ... while k is forced by (0,0,2) and carries amplitude 0: the forgotten descendant
    # m = 2: the forgotten variety is exactly {q0 = q1 = (0,0,+-1)} — coincident recruits, i.e. the
    # m = 1 point with a duplicated address (the O_- anchor x recruit outside target forces
    # |q_j|^2 = 1 and x_j y_j = 0; antipodal recruits q1 = -q0 are excluded by t.t != 0 on t = q0 + q1).
    # No genuinely two-recruit forgotten point exists on this skeleton.
    res2 = results[('onesided', 2)]
    x0, x1, yy0, yy1, s0, s1, z1 = sp.symbols('x0 x1 yy0 yy1 s0 s1 z1')
    G2 = set(res2['forgotten_gb'].exprs)
    for marker in (x0, x1, yy0 - z1, yy1 - z1, z1**2 - 1):
        assert marker in G2, ('m=2 forgotten variety marker missing', marker)
    assert verify_point('onesided', 2, res2, {x0: 0, x1: 0, yy0: 1, yy1: 1, s0: 1, s1: 1})
    print('F2 forgotten-case real witnesses re-verified by substitution: m=1 q0=(0,0,+-1), b0=a+, c=0 '
          '(all outside forcing 0, k forced by (0,0,2), k empty); m=2 forgotten variety = coincident '
          'recruits q0 = q1 = (0,0,+-1) only (duplicate of the m=1 point)')

    print('verdict table (per fixture: A = core ACTIVE, B = core empty & F(k)=0, forgotten = core empty & F(k)!=0):')
    for (kind, m), res in results.items():
        print(f'  {kind:9s} m={m}: A {res["A"]:6s} B {res["B"]:6s} forgotten {res["forgotten"]}')
    print('rule: a closure point is valid only under A or B; every forgotten SAT is an INVALID CLOSURE TEST')
    print('claim boundary: ONE skeleton, m <= 3, finite_diagnostic; RSC-O global / OCSR / WS / G6/G7 / Clay OPEN')
    print(f'total time {time.time() - T0:.1f}s')
    print('NS P2 FORCED-ADDRESS ACCOUNTING PASS')


if __name__ == '__main__':
    main()
