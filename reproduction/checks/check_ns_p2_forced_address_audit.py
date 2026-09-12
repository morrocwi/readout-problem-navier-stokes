#!/usr/bin/env python3
"""Per-ADDRESS forced-address accounting classifier (PROP-P3-FORCED-ADDRESS-AUDIT-01) and the
isotropic-saturation invariant (PROP-P3-ISOTROPIC-SATURATION-INVARIANT-01).

Unit of accounting = ONE ADDRESS after aggregation of every pair contribution that lands on it.
States are mutually exclusive and decided in this precedence order:

  ISOTROPIC_TARGET      t.t = 0 with t != 0 (degenerate projection; complex only).  Flagged first;
                        never counted as zero or nonzero.  This is the checker form of the isotropic
                        guard that corrected the raw single-O reading in the merged accounting-rule
                        paper (paper/NS_P2_FORCED_ADDRESS_ACCOUNTING_RULE.md, fixture F1).
  ACTIVE                a is registered in the web and its amplitude is != 0.
  EXACT_CANCELLED       F(a) = 0 exactly with >= 2 individually nonzero contributions.
  NULL_BY_GEOMETRY      F(a) = 0 exactly and every contribution is individually 0.
  TED                   F(a) != 0, a not registered, a outside the declared cell (registered exit).
  FORGOTTEN_REGISTERED  F(a) != 0, a registered, amplitude = 0      -> INVALID CLOSURE TEST.
  FORGOTTEN_INSIDE      F(a) != 0, a not registered, a inside the declared cell
                                                                    -> INVALID CLOSURE TEST.

Exact inputs (sympy rationals / algebraic numbers) are decided exactly; there is no tolerance in
any exact decision.  Float inputs go through a separate path whose zero state is
NUMERICAL_ZERO(eps): it is reported with its eps and is never renamed EXACT_CANCELLED or
NULL_BY_GEOMETRY.

Every record carries (a, N_terms, F(a), registered, state).

Fixtures run in CI (all exact, finite_diagnostic):
  * W1, W2, W3 point A -- the three open seeds of the multi-source cancellation lane; expected
    INVALID with 10 / 12 / 18 FORGOTTEN_INSIDE addresses.  These counts are the calibration of the
    classifier against the internal run record, not a result about the seeds.
  * a deterministic subset of 20 of the 610 NPSC box-2 SELF_CLOSED_PRODUCTIVE hits (fixed index
    rule (k * 610) // 20, k = 0..19, over the box-2 hit list in file order), reconstructed with
    the sweep's own perp_basis (copied verbatim below); each must be INVALID with >= 1
    FORGOTTEN_REGISTERED address.
  * an isotropic complex target, a float NUMERICAL_ZERO control, and the saturation invariant.

The full 610/610 INVALID result is a FINITE_DIAGNOSTIC record of the internal run and is printed,
not re-run, here.  Box-1 hits (12) were not re-audited.  Depth 1 only.  This instrument proves
nothing about OCSR, Witness Soundness, G6/G7 or Clay Navier-Stokes regularity.
"""
import itertools
import json
import sys
import time
from collections import Counter

import sympy as sp

T0 = time.time()

# ---------------------------------------------------------------------------------------------
# Bilinear interaction.  Exact Leray form (division by k.k) for exact classification;
# denominator-cleared form for the symbolic saturation invariant.
# ---------------------------------------------------------------------------------------------

def proj(v, k):
    return v - (v.dot(k) / k.dot(k)) * k


def B(p, q, a, b):
    return proj((a.dot(q)) * b + (b.dot(p)) * a, p + q)


def proj_dc(v, k):
    return (k.dot(k)) * v - (v.dot(k)) * k


def B_dc(p, q, a, b):
    return proj_dc((a.dot(q)) * b + (b.dot(p)) * a, p + q)


def V(*xs):
    return sp.Matrix([sp.nsimplify(x) for x in xs])


ZERO3 = sp.zeros(3, 1)


# ---------------------------------------------------------------------------------------------
# Generator basis, copied VERBATIM from the internal NPSC sweep record (rg_npsc_sweep.py,
# functions cross / parallel / perp_basis).  Point coordinates (x_i, y_i) of a hit are
# coefficients in THIS basis; a different basis of m^perp changes the amplitude and the verdict.
# ---------------------------------------------------------------------------------------------

def cross(p, q):
    return (p[1]*q[2]-p[2]*q[1], p[2]*q[0]-p[0]*q[2], p[0]*q[1]-p[1]*q[0])

def parallel(p, q):
    return cross(p, q) == (0, 0, 0)

def perp_basis(m):
    """two independent integer vectors perpendicular to lattice vector m (exact)."""
    m1, m2, m3 = m
    cands = [(m2, -m1, 0), (m3, 0, -m1), (0, m3, -m2), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    cands = [c for c in cands if sum(x*y for x, y in zip(c, m)) == 0 and c != (0, 0, 0)]
    for c1, c2 in itertools.combinations(cands, 2):
        if not parallel(c1, c2):
            return c1, c2
    raise RuntimeError(m)


# ---------------------------------------------------------------------------------------------
# The classifier
# ---------------------------------------------------------------------------------------------

INVALID_STATES = ('FORGOTTEN_REGISTERED', 'FORGOTTEN_INSIDE')


def aggregate(modes):
    """modes: dict label -> (address Matrix, amplitude Matrix).  Every unordered pair of labels,
    self-pairs included, contributes B(p,q,a,b) to the address p+q.  Returns
    {address tuple: {'t': Matrix, 'iso': bool, 'terms': [Matrix]}}."""
    labels = list(modes)
    acc = {}
    for m, n in itertools.combinations_with_replacement(labels, 2):
        p, a = modes[m]
        q, b = modes[n]
        t = p + q
        if t == ZERO3:
            continue                                  # p + (-p): no target
        key = tuple(t)
        if t.dot(t) == 0:
            acc.setdefault(key, {'t': t, 'iso': True, 'terms': []})
            continue                                  # isotropic: projection undefined; flagged
        rec = acc.setdefault(key, {'t': t, 'iso': False, 'terms': []})
        rec['terms'].append(B(p, q, a, b).applyfunc(sp.nsimplify))
    return acc


def classify_exact(modes, cell_n2):
    """Exact per-address classification.  cell_n2 = declared cell as a bound on |t|^2."""
    acc = aggregate(modes)
    reg = {tuple(k): amp for (k, amp) in modes.values()}
    out = []
    for key, rec in acc.items():
        t = rec['t']
        if rec['iso']:
            out.append(dict(a=str(key), N=len(rec['terms']), n_nonzero=None, F=None,
                            registered=key in reg, state='ISOTROPIC_TARGET'))
            continue
        F = sum(rec['terms'], ZERO3).applyfunc(sp.simplify)
        nz = [x for x in rec['terms'] if x.applyfunc(sp.simplify) != ZERO3]
        Fz = (F == ZERO3)
        registered = key in reg
        amp_nonzero = registered and reg[key] != ZERO3
        if registered and amp_nonzero:
            st = 'ACTIVE'
        elif Fz:
            st = 'EXACT_CANCELLED' if len(nz) >= 2 else 'NULL_BY_GEOMETRY'
        elif registered:
            st = 'FORGOTTEN_REGISTERED'
        elif t.dot(t) > cell_n2:
            st = 'TED'
        else:
            st = 'FORGOTTEN_INSIDE'
        out.append(dict(a=str(key), N=len(rec['terms']), n_nonzero=len(nz),
                        F=[str(x) for x in F], registered=registered, state=st))
    return out


def classify_float(records, eps):
    """Float path.  records: list of dicts with keys a, registered, amp_nonzero (bool: amplitude
    bitwise nonzero), F (list of 3 complex or floats), inside (bool: inside declared cell).
    Zero decisions use |F| <= eps and are reported as NUMERICAL_ZERO(eps), never as EXACT."""
    out = []
    for r in records:
        Fabs = max(abs(complex(x)) for x in r['F'])
        if r['registered'] and r['amp_nonzero']:
            st = 'ACTIVE'
        elif Fabs <= eps:
            st = 'NUMERICAL_ZERO'
        elif r['registered']:
            st = 'FORGOTTEN_REGISTERED'
        elif not r['inside']:
            st = 'TED'
        else:
            st = 'FORGOTTEN_INSIDE'
        out.append(dict(a=r['a'], N=r.get('N'), F=[str(x) for x in r['F']], Fabs=Fabs,
                        F_bitwise_zero=(Fabs == 0.0), registered=r['registered'], state=st, eps=eps))
    return out


def verdict(recs):
    c = Counter(r['state'] for r in recs)
    inv = sum(c.get(s, 0) for s in INVALID_STATES)
    return c, inv


def summarize(name, recs):
    c, inv = verdict(recs)
    tag = 'VALID CLOSURE TEST' if inv == 0 else f'INVALID CLOSURE TEST ({inv} forgotten forced addresses)'
    print(f'{name}: addresses={len(recs)} {dict(c)} -> {tag}')
    return c, inv


# ---------------------------------------------------------------------------------------------
# Isotropic-saturation invariant (checker form).  For every symbolic pair sum t used with the
# denominator-cleared projection, adjoin u_t * (t.t) - 1 (or assert t.t != 0 numerically).
# ---------------------------------------------------------------------------------------------

def isotropic_saturation(targets, prefix='u_iso'):
    """targets: list of symbolic 3-vectors.  Returns (polys, gens) with polys = [u_i*(t_i.t_i) - 1]."""
    us = sp.symbols(f'{prefix}0:{len(targets)}')
    polys = [sp.expand(u * t.dot(t) - 1) for u, t in zip(us, targets)]
    return polys, list(us)


# ---------------------------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------------------------

def fixture_W1():
    W1 = [(V(1, 1, 0), V(0, -1, 0), V(-1, 1, -1), V(1, 0, 1)),
          (V(1, 0, 1), V(0, 0, -1), V(-1, 1, 1), V(2, 3, 0))]
    m = {}
    for i, (p, q, a, b) in enumerate(W1):
        m[f'p{i}'] = (p, a); m[f'-p{i}'] = (-p, a); m[f'q{i}'] = (q, b); m[f'-q{i}'] = (-q, b)
    return m, sp.Integer(3)


def fixture_W2():
    k2 = V(1, 1, 1)
    W2 = [(V(1, 0, 0), V(0, 66, -22), V(1, -1, 1)),
          (V(0, 1, 0), V(1, 0, 2), V(-2, 1, 2)),
          (V(0, 0, 1), V(3, 1, 0), V(-2, 2, 1))]
    m = {}
    for i, (p, a, b) in enumerate(W2):
        q = k2 - p
        m[f'p{i}'] = (p, a); m[f'-p{i}'] = (-p, a); m[f'q{i}'] = (q, b); m[f'-q{i}'] = (-q, b)
    return m, sp.Integer(3)


# W3 point A: the frozen T0-02 seed (14 modes on the sqrt3-lattice), exact wavevectors and
# amplitude vectors, as in the internal record; declared cell |t|^2 < 29/10.
W3_SEED = {
 "p0": [
  [
   "sqrt(3)/2",
   "0",
   "1/2"
  ],
  [
   "0",
   "1",
   "0"
  ]
 ],
 "-p0": [
  [
   "-sqrt(3)/2",
   "0",
   "-1/2"
  ],
  [
   "0",
   "1",
   "0"
  ]
 ],
 "q0": [
  [
   "-sqrt(3)/2",
   "0",
   "1/2"
  ],
  [
   "1/2",
   "0",
   "sqrt(3)/2"
  ]
 ],
 "-q0": [
  [
   "sqrt(3)/2",
   "0",
   "-1/2"
  ],
  [
   "1/2",
   "0",
   "sqrt(3)/2"
  ]
 ],
 "p1": [
  [
   "-sqrt(3)/4",
   "3/4",
   "1/2"
  ],
  [
   "-sqrt(3)/2",
   "-1/2",
   "0"
  ]
 ],
 "-p1": [
  [
   "sqrt(3)/4",
   "-3/4",
   "-1/2"
  ],
  [
   "-sqrt(3)/2",
   "-1/2",
   "0"
  ]
 ],
 "q1": [
  [
   "sqrt(3)/4",
   "-3/4",
   "1/2"
  ],
  [
   "-1/4",
   "sqrt(3)/4",
   "sqrt(3)/2"
  ]
 ],
 "-q1": [
  [
   "-sqrt(3)/4",
   "3/4",
   "-1/2"
  ],
  [
   "-1/4",
   "sqrt(3)/4",
   "sqrt(3)/2"
  ]
 ],
 "p2": [
  [
   "-sqrt(3)/4",
   "-3/4",
   "1/2"
  ],
  [
   "sqrt(3)/2",
   "-1/2",
   "0"
  ]
 ],
 "-p2": [
  [
   "sqrt(3)/4",
   "3/4",
   "-1/2"
  ],
  [
   "sqrt(3)/2",
   "-1/2",
   "0"
  ]
 ],
 "q2": [
  [
   "sqrt(3)/4",
   "3/4",
   "1/2"
  ],
  [
   "-1/4",
   "-sqrt(3)/4",
   "sqrt(3)/2"
  ]
 ],
 "-q2": [
  [
   "-sqrt(3)/4",
   "-3/4",
   "-1/2"
  ],
  [
   "-1/4",
   "-sqrt(3)/4",
   "sqrt(3)/2"
  ]
 ],
 "k": [
  [
   "0",
   "0",
   "1"
  ],
  [
   "1",
   "0",
   "0"
  ]
 ],
 "-k": [
  [
   "0",
   "0",
   "-1"
  ],
  [
   "1",
   "0",
   "0"
  ]
 ]
}


def fixture_W3A():
    m = {}
    for lbl, (k_exact, amp) in W3_SEED.items():
        m[lbl] = (V(*[sp.sympify(x) for x in k_exact]), V(*[sp.sympify(x) for x in amp]))
    return m, sp.Rational(29, 10)


# NPSC box-2 hits: 20 of 610, fixed index rule (k*610)//20 over the box-2 hit list in file order
# (rg_npsc_results_box2_s3.json then rg_npsc_results_box2_s4.json of the internal record).
NPSC_SUBSET = [
 {
  "hit_index": 0,
  "S_reps": [
   [
    -2,
    -2,
    -2
   ],
   [
    -2,
    -1,
    0
   ],
   [
    0,
    -1,
    -2
   ]
  ],
  "point": {
   "x0": "0",
   "y0": "0",
   "x1": "-1",
   "y1": "0",
   "x2": "0",
   "y2": "-1"
  }
 },
 {
  "hit_index": 30,
  "S_reps": [
   [
    -2,
    -2,
    -2
   ],
   [
    -2,
    -2,
    0
   ],
   [
    -2,
    0,
    0
   ],
   [
    0,
    -2,
    0
   ]
  ],
  "point": {
   "x0": "0",
   "y0": "0",
   "x1": "0",
   "y1": "0",
   "x2": "-1",
   "y2": "-1",
   "x3": "-1",
   "y3": "1"
  }
 },
 {
  "hit_index": 61,
  "S_reps": [
   [
    -2,
    -2,
    -2
   ],
   [
    -2,
    -1,
    0
   ],
   [
    -2,
    2,
    0
   ],
   [
    0,
    -1,
    -2
   ]
  ],
  "point": {
   "x0": "0",
   "y0": "0",
   "x1": "-1",
   "y1": "0",
   "x2": "0",
   "y2": "0",
   "x3": "0",
   "y3": "-1"
  }
 },
 {
  "hit_index": 91,
  "S_reps": [
   [
    -2,
    -2,
    -2
   ],
   [
    -2,
    0,
    1
   ],
   [
    -2,
    2,
    0
   ],
   [
    0,
    -2,
    1
   ]
  ],
  "point": {
   "x0": "0",
   "y0": "0",
   "x1": "-1",
   "y1": "0",
   "x2": "0",
   "y2": "0",
   "x3": "-1",
   "y3": "-1"
  }
 },
 {
  "hit_index": 122,
  "S_reps": [
   [
    -2,
    -2,
    -1
   ],
   [
    -2,
    -2,
    1
   ],
   [
    -1,
    -1,
    -1
   ],
   [
    0,
    0,
    -2
   ]
  ],
  "point": {
   "x0": "-2",
   "y0": "2",
   "x1": "-1",
   "y1": "2",
   "x2": "0",
   "y2": "0",
   "x3": "0",
   "y3": "0"
  }
 },
 {
  "hit_index": 152,
  "S_reps": [
   [
    -2,
    -2,
    -1
   ],
   [
    -2,
    -1,
    -2
   ],
   [
    -1,
    1,
    1
   ],
   [
    0,
    -1,
    1
   ]
  ],
  "point": {
   "x0": "-2",
   "y0": "1",
   "y1": "3",
   "x1": "-129/8",
   "x2": "0",
   "y2": "0",
   "x3": "0",
   "y3": "0"
  }
 },
 {
  "hit_index": 183,
  "S_reps": [
   [
    -2,
    -2,
    -1
   ],
   [
    -2,
    -1,
    1
   ],
   [
    -2,
    1,
    -1
   ],
   [
    0,
    -2,
    2
   ]
  ],
  "point": {
   "x0": "0",
   "y0": "0",
   "x1": "-1",
   "y1": "0",
   "x2": "-1",
   "y2": "0",
   "x3": "0",
   "y3": "0"
  }
 },
 {
  "hit_index": 213,
  "S_reps": [
   [
    -2,
    -2,
    -1
   ],
   [
    -2,
    0,
    2
   ],
   [
    -2,
    2,
    0
   ],
   [
    0,
    -2,
    2
   ]
  ],
  "point": {
   "x0": "0",
   "y0": "0",
   "x1": "-2",
   "y1": "0",
   "x2": "-2",
   "y2": "1",
   "x3": "0",
   "y3": "0"
  }
 },
 {
  "hit_index": 244,
  "S_reps": [
   [
    -2,
    -2,
    -1
   ],
   [
    -1,
    1,
    -1
   ],
   [
    -1,
    1,
    1
   ],
   [
    0,
    0,
    -2
   ]
  ],
  "point": {
   "x0": "0",
   "y0": "0",
   "x1": "-1",
   "y1": "-1",
   "x2": "0",
   "y2": "-1",
   "x3": "0",
   "y3": "0"
  }
 },
 {
  "hit_index": 274,
  "S_reps": [
   [
    -2,
    -2,
    0
   ],
   [
    -2,
    0,
    -2
   ],
   [
    -2,
    0,
    0
   ],
   [
    0,
    -2,
    0
   ]
  ],
  "point": {
   "x0": "0",
   "y0": "0",
   "x1": "0",
   "y1": "0",
   "x2": "-1",
   "y2": "-1",
   "x3": "-1",
   "y3": "1"
  }
 },
 {
  "hit_index": 305,
  "S_reps": [
   [
    -2,
    -2,
    0
   ],
   [
    -2,
    0,
    -1
   ],
   [
    -1,
    0,
    1
   ],
   [
    0,
    -2,
    1
   ]
  ],
  "point": {
   "x0": "0",
   "y0": "0",
   "x1": "-1",
   "y1": "0",
   "x2": "0",
   "y2": "0",
   "x3": "-1",
   "y3": "1"
  }
 },
 {
  "hit_index": 335,
  "S_reps": [
   [
    -2,
    -2,
    0
   ],
   [
    -2,
    1,
    -1
   ],
   [
    -2,
    1,
    1
   ],
   [
    0,
    0,
    -2
   ]
  ],
  "point": {
   "x1": "-2",
   "y1": "1",
   "y2": "3",
   "x0": "0",
   "y0": "0",
   "x2": "-36/5",
   "x3": "0",
   "y3": "0"
  }
 },
 {
  "hit_index": 366,
  "S_reps": [
   [
    -2,
    -2,
    0
   ],
   [
    -1,
    -1,
    -1
   ],
   [
    -1,
    -1,
    1
   ],
   [
    -1,
    1,
    0
   ]
  ],
  "point": {
   "x0": "0",
   "y0": "0",
   "x1": "-1",
   "y1": "-1",
   "x2": "-1",
   "y2": "1",
   "x3": "0",
   "y3": "0"
  }
 },
 {
  "hit_index": 396,
  "S_reps": [
   [
    -2,
    -1,
    -1
   ],
   [
    -2,
    -1,
    1
   ],
   [
    -2,
    0,
    0
   ],
   [
    0,
    0,
    -2
   ]
  ],
  "point": {
   "x0": "-2",
   "y0": "1",
   "y1": "3",
   "x1": "-24/5",
   "x2": "0",
   "y2": "0",
   "x3": "0",
   "y3": "0"
  }
 },
 {
  "hit_index": 427,
  "S_reps": [
   [
    -2,
    -1,
    -1
   ],
   [
    -2,
    0,
    0
   ],
   [
    -1,
    -2,
    1
   ],
   [
    -1,
    1,
    -2
   ]
  ],
  "point": {
   "x0": "-1",
   "y0": "0",
   "x1": "0",
   "y1": "0",
   "x2": "-1",
   "y2": "0",
   "x3": "0",
   "y3": "0"
  }
 },
 {
  "hit_index": 457,
  "S_reps": [
   [
    -2,
    -1,
    -1
   ],
   [
    -2,
    0,
    1
   ],
   [
    -1,
    2,
    1
   ],
   [
    0,
    -1,
    -2
   ]
  ],
  "point": {
   "x1": "3",
   "y1": "3",
   "y3": "-3",
   "x0": "0",
   "y0": "0",
   "x2": "0",
   "y2": "0",
   "x3": "-57/4"
  }
 },
 {
  "hit_index": 488,
  "S_reps": [
   [
    -2,
    -1,
    -1
   ],
   [
    -1,
    -2,
    1
   ],
   [
    -1,
    -1,
    -1
   ],
   [
    -1,
    1,
    -2
   ]
  ],
  "point": {
   "x0": "-1",
   "y0": "0",
   "x1": "-1",
   "y1": "0",
   "x2": "0",
   "y2": "0",
   "x3": "0",
   "y3": "0"
  }
 },
 {
  "hit_index": 518,
  "S_reps": [
   [
    -2,
    -1,
    -1
   ],
   [
    0,
    -2,
    -1
   ],
   [
    0,
    -2,
    1
   ],
   [
    0,
    0,
    -2
   ]
  ],
  "point": {
   "x0": "0",
   "y0": "0",
   "x1": "-1",
   "y1": "-1",
   "x2": "-1",
   "y2": "-1",
   "x3": "0",
   "y3": "0"
  }
 },
 {
  "hit_index": 549,
  "S_reps": [
   [
    -2,
    -1,
    0
   ],
   [
    -2,
    1,
    0
   ],
   [
    -1,
    -2,
    0
   ],
   [
    -1,
    1,
    0
   ]
  ],
  "point": {
   "x0": "-2",
   "y0": "-2",
   "x1": "0",
   "y1": "0",
   "x2": "-1",
   "y2": "-2",
   "x3": "0",
   "y3": "0"
  }
 },
 {
  "hit_index": 579,
  "S_reps": [
   [
    -2,
    -1,
    0
   ],
   [
    0,
    -2,
    0
   ],
   [
    0,
    -1,
    -1
   ],
   [
    0,
    -1,
    1
   ]
  ],
  "point": {
   "x0": "0",
   "y0": "0",
   "x1": "0",
   "y1": "0",
   "x2": "-1",
   "y2": "-1",
   "x3": "-1",
   "y3": "1"
  }
 }
]
NPSC_BOX = 2
NPSC_FULL_RECORD = {'hits': 610, 'invalid': 610, 'valid': 0,
                    'address_states': {'NULL_BY_GEOMETRY': 15186, 'ACTIVE': 2440, 'FORGOTTEN_REGISTERED': 1260},
                    'tier': 'FINITE_DIAGNOSTIC (internal run record, not re-run in CI)',
                    'box1_hits_not_reaudited': 12}


def fixture_npsc(hit):
    reps = [tuple(v) for v in hit['S_reps']]
    pt = hit['point']
    m = {}
    for i, v in enumerate(reps):
        k = V(*v)
        c1, c2 = perp_basis(v)                        # the sweep's basis, not any other
        amp = sp.nsimplify(pt.get(f'x{i}', 0)) * V(*c1) + sp.nsimplify(pt.get(f'y{i}', 0)) * V(*c2)
        assert amp.dot(k) == 0
        m[str(v)] = (k, amp)
        m['-' + str(v)] = (-k, amp)                   # real field: a_{-m} = a_m
    return m, sp.Integer(3 * NPSC_BOX * NPSC_BOX)


# ---------------------------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------------------------

def main():
    report = {'tier': 'finite_diagnostic', 'fixtures': {}, 'npsc_subset': [], 'npsc_full_record': NPSC_FULL_RECORD}
    expected = {'W1': (26, {'NULL_BY_GEOMETRY': 8, 'EXACT_CANCELLED': 2, 'TED': 6, 'FORGOTTEN_INSIDE': 10}, 10),
                'W2': (56, {'NULL_BY_GEOMETRY': 12, 'EXACT_CANCELLED': 2, 'FORGOTTEN_INSIDE': 12, 'ACTIVE': 12, 'TED': 18}, 12),
                'W3A': (82, {'NULL_BY_GEOMETRY': 22, 'ACTIVE': 14, 'TED': 28, 'FORGOTTEN_INSIDE': 18}, 18)}
    for name, fx in (('W1', fixture_W1), ('W2', fixture_W2), ('W3A', fixture_W3A)):
        modes, cell = fx()
        recs = classify_exact(modes, cell)
        c, inv = summarize(f'{name} cell |t|^2 <= {cell}', recs)
        n_exp, c_exp, inv_exp = expected[name]
        assert len(recs) == n_exp and dict(c) == c_exp and inv == inv_exp, (name, len(recs), dict(c), inv)
        assert inv > 0, name                          # open seeds: INVALID by calibration
        report['fixtures'][name] = {'addresses': len(recs), 'states': dict(c), 'invalid': inv, 'records': recs}
    print(f'[fixtures W1/W2/W3A calibrated against the internal record] {time.time() - T0:.1f}s')

    # NPSC subset
    tot = Counter()
    for hit in NPSC_SUBSET:
        modes, cell = fixture_npsc(hit)
        recs = classify_exact(modes, cell)
        c, inv = verdict(recs)
        tot.update(c)
        n_fr = c.get('FORGOTTEN_REGISTERED', 0)
        assert inv >= 1 and n_fr >= 1, (hit['hit_index'], dict(c))
        # calibration of the subset against the record: one forgotten +- pair, two populated +- pairs,
        # every unregistered target geometrically null
        assert n_fr == 2 and c.get('ACTIVE') == 4 and set(c) <= {'NULL_BY_GEOMETRY', 'ACTIVE', 'FORGOTTEN_REGISTERED'}, (hit['hit_index'], dict(c))
        assert 'ISOTROPIC_TARGET' not in c, hit['hit_index']
        report['npsc_subset'].append({'hit_index': hit['hit_index'], 'S_reps': hit['S_reps'], 'states': dict(c), 'invalid': inv})
        print(f"NPSC hit #{hit['hit_index']:3d} S={hit['S_reps']} addresses={len(recs)} {dict(c)} -> INVALID ({inv})")
    print(f'NPSC subset: {len(NPSC_SUBSET)}/{len(NPSC_SUBSET)} INVALID; address states total {dict(tot)}')
    print(f'NPSC full internal record (not re-run): {NPSC_FULL_RECORD}')
    print(f'[npsc subset] {time.time() - T0:.1f}s')

    # Isotropic complex target: the guard fires before any zero/nonzero decision.
    I = sp.I
    iso = {'p': (V(1, 0, 0), V(0, 0, 1)), 'q': (sp.Matrix([0, I, 0]), V(0, 0, 1))}
    t = iso['p'][0] + iso['q'][0]
    assert t.dot(t) == 0 and t != ZERO3
    recs = classify_exact(iso, sp.Integer(3))
    states = {r['a']: r['state'] for r in recs}
    assert states[str(tuple(t))] == 'ISOTROPIC_TARGET', states
    # saturation invariant refuses this point: u*(t.t) - 1 = -1 != 0 for every u
    polys, us = isotropic_saturation([t])
    assert polys[0] == -1                          # constant after expansion: no u satisfies it
    # and on a real lattice target it is satisfiable exactly (u = 1/(t.t))
    tr = V(1, 1, 0)
    polys_r, us_r = isotropic_saturation([tr])
    assert polys_r[0].subs({us_r[0]: sp.Rational(1, 2)}) == 0
    # the denominator-cleared projection is rank-one on the isotropic direction: P_dc[t] = 0 for t.t = 0
    assert proj_dc(t, t) == ZERO3
    print('isotropic guard: ISOTROPIC_TARGET flagged for t = (1, i, 0); saturation polynomial u*(t.t)-1 refuses it; PASS')

    # Float control: a numerically zero forcing is NUMERICAL_ZERO(eps), never EXACT.
    frec = [dict(a='(1,0,0)', N=2, registered=False, amp_nonzero=False, F=[1e-15, 0.0, 0.0], inside=True),
            dict(a='(0,1,0)', N=1, registered=True, amp_nonzero=False, F=[0.5, 0.0, 0.0], inside=True),
            dict(a='(0,0,3)', N=1, registered=False, amp_nonzero=False, F=[0.5, 0.0, 0.0], inside=False),
            dict(a='(1,1,0)', N=1, registered=True, amp_nonzero=True, F=[0.5, 0.0, 0.0], inside=True)]
    fr = classify_float(frec, eps=1e-12)
    fs = [r['state'] for r in fr]
    assert fs == ['NUMERICAL_ZERO', 'FORGOTTEN_REGISTERED', 'TED', 'ACTIVE'], fs
    assert all(r['state'] not in ('EXACT_CANCELLED', 'NULL_BY_GEOMETRY') for r in fr)
    assert fr[0]['F_bitwise_zero'] is False
    print('float control: NUMERICAL_ZERO(eps=1e-12) kept separate from EXACT states; PASS')

    report['wall_s'] = round(time.time() - T0, 1)
    if '--json' in sys.argv:
        json.dump(report, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1, default=str)
    print(f'NS P2 FORCED-ADDRESS AUDIT (per-address classifier) PASS in {report["wall_s"]}s')


if __name__ == '__main__':
    main()
