#!/usr/bin/env python3
"""Exact W1/W2/W3 witness-soundness audit for NS P2.

Reuse-first purpose:
- reuse the existing exact cancellation witnesses W1/W2/W3;
- do NOT treat C_k > 0 as automatically being a physical defect;
- test the missing concrete question: can exact cancellation at the shared
  target erase the source web after one full local-convolution generation?

All PASS decisions use exact SymPy arithmetic.
"""

import itertools
import sympy as sp

R3 = sp.sqrt(3)


def V(*xs):
    return sp.Matrix([sp.nsimplify(x) for x in xs])


def proj(v, k):
    return sp.simplify(v - (v.dot(k) / k.dot(k)) * k)


def B(p, q, a, b):
    """Symmetric incompressible NSE triad interaction into k=p+q."""
    k = p + q
    return sp.simplify(proj((a.dot(q)) * b + (b.dot(p)) * a, k))


def full_depth1(real_modes):
    """Exact target ledger for one full convolution generation."""
    mode_map = {}
    for m, u in real_modes:
        for mm, uu in ((m, u), (-m, u)):
            key = tuple(mm)
            mode_map[key] = sp.simplify(
                mode_map.get(key, sp.zeros(3, 1)) + uu
            )

    modes = [
        (sp.Matrix(key), u)
        for key, u in mode_map.items()
        if u != sp.zeros(3, 1)
    ]

    targets = {}
    for (m1, u1), (m2, u2) in itertools.combinations(modes, 2):
        t = sp.simplify(m1 + m2)
        if t == sp.zeros(3, 1):
            continue
        f = B(m1, m2, u1, u2)
        targets.setdefault(tuple(t), []).append(f)

    ledger = {}
    for key, srcs in targets.items():
        ledger[key] = {
            "multiplicity": len(srcs),
            "net": sp.simplify(sum(srcs, sp.zeros(3, 1))),
        }
    return modes, ledger


def audit(
    name,
    k,
    sources,
    expected_targets,
    expected_nonzero,
    expected_single,
    expected_extra_zero,
):
    parent = [B(p, q, a, b) for p, q, a, b in sources]
    assert all(g != sp.zeros(3, 1) for g in parent)
    assert sp.simplify(sum(parent, sp.zeros(3, 1))) == sp.zeros(3, 1)

    real_modes = [(p, a) for p, q, a, b in sources]
    real_modes += [(q, b) for p, q, a, b in sources]
    modes, ledger = full_depth1(real_modes)

    assert len(ledger) == expected_targets
    kp, km = tuple(k), tuple(-k)
    assert ledger[kp]["net"] == sp.zeros(3, 1)
    assert ledger[km]["net"] == sp.zeros(3, 1)

    nonzero = 0
    single = 0
    extra_zero = []
    for key, row in ledger.items():
        if row["net"] != sp.zeros(3, 1):
            nonzero += 1
            if row["multiplicity"] == 1:
                single += 1
        elif key not in (kp, km):
            extra_zero.append(key)

    assert nonzero == expected_nonzero
    assert single == expected_single
    assert len(extra_zero) == expected_extra_zero

    return {
        "name": name,
        "modes": len(modes),
        "targets": len(ledger),
        "nonzero_targets": nonzero,
        "single_source_nonzero_targets": single,
        "extra_zero_targets": len(extra_zero),
    }


# W1: existing two-shell N=2 cancellation witness.
k1 = V(1, 0, 0)
W1 = [
    (V(1, 1, 0), V(0, -1, 0), V(-1, 1, -1), V(1, 0, 1)),
    (V(1, 0, 1), V(0, 0, -1), V(-1, 1, 1), V(2, 3, 0)),
]

# W2: existing rank-2 generic cancellation witness.
k2 = V(1, 1, 1)
W2raw = [
    (V(1, 0, 0), V(0, 66, -22), V(1, -1, 1)),
    (V(0, 1, 0), V(1, 0, 2), V(-2, 1, 2)),
    (V(0, 0, 1), V(3, 1, 0), V(-2, 2, 1)),
]
W2 = [(p, k2 - p, a, b) for p, a, b in W2raw]

# W3: existing equal-shell N=3 cancellation witness.
k3 = V(0, 0, 1)
thetas = [0, 2 * sp.pi / 3, 4 * sp.pi / 3]


def e_th(th):
    return sp.Matrix([-sp.sin(th), sp.cos(th), 0])


def p_th(th):
    return sp.Matrix([
        R3 / 2 * sp.cos(th),
        R3 / 2 * sp.sin(th),
        sp.Rational(1, 2),
    ])


W3 = []
for th in thetas:
    p = p_th(th)
    q = k3 - p
    e = e_th(th)
    W3.append((p, q, e, -(q.cross(e))))


results = [
    audit(
        "W1", k1, W1,
        expected_targets=18,
        expected_nonzero=16,
        expected_single=12,
        expected_extra_zero=0,
    ),
    audit(
        "W2", k2, W2,
        expected_targets=44,
        expected_nonzero=42,
        expected_single=30,
        expected_extra_zero=0,
    ),
    audit(
        "W3", k3, W3,
        expected_targets=44,
        expected_nonzero=36,
        expected_single=30,
        expected_extra_zero=6,
    ),
]

print("NS P2 W1/W2/W3 cancellation-constraint audit: PASS")
for row in results:
    print(
        f"{row['name']}: modes={row['modes']} "
        f"targets={row['targets']} "
        f"nonzero={row['nonzero_targets']} "
        f"single-source-nonzero={row['single_source_nonzero_targets']} "
        f"extra-zero={row['extra_zero_targets']}"
    )
print("Exact cancellation at +/-k is not one-generation losslessness on W1/W2/W3.")
print("C_k > 0 is NOT promoted to physical defect; the cancellation is a live exact constraint.")
