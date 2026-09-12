#!/usr/bin/env python3
"""M3 suppression-label checker: multi-label O/E/C/T + UNRESOLVED, double-O rank counter.

Proposal id: PROP-P3-M3-SUPPRESSION-LABELS-01 (not yet in Toledo).
Paper: paper/NS_P2_M3_SUPPRESSION_LABELS.md
Parent interface: paper/NS_P2_RECURSIVE_SUPPRESSION_CHARGING_CARD.md (M3 label-set semantics).

For a finite registered web of real modes (u(-m) = u(m), exact amplitudes over Q(sqrt3) / Q(sqrt5)),
enumerate every target t = p + q of one full local convolution generation and classify
every SUPPRESSED target (net forcing exactly zero while at least one pair lands on t)
by a LABEL SET L(t), a subset of {O, E, C, T}:

  O  ORTH      some contributing pair has a.q = 0 or b.p = 0   (anchor-cross orthogonality nullity)
  E  EQSHELL   some contributing pair has |p| = |q|            (equal-shell nullity / direction lock)
  C  MSCANCEL  >= 2 contributions individually nonzero, net exactly zero
  T  TED       target lies outside the declared cell (registered exit; terminal / named defect
               require external declarations and are not derived here)

  UNRESOLVED   suppression observed, none of the four labels provable from the data (fail-closed)

Labels are NOT mutually exclusive: a target may carry {O, E, T}, {E, C}, {O, E, C}, and so on.

C is an ACCOUNTING label, never a physical loss.  It records that several individually
productive contributions sum to exactly zero at one target.  Whether such a cancellation is a
payable loss (D_cancel) or an amplitude constraint (F_e = 0) is exactly Witness Soundness,
which is OPEN; nothing in this file promotes C to a loss, a defect, or a phase tax.

Double-O counter (per suppressed target e):
  O(e) = set of retained anchors (m, a_m) whose interaction with a recruit is O-suppressed,
         i.e. the anchor polarization annihilates the partner wavevector (a_m . q = 0).
  "double-O" means rank{a_m : m in O(e)} >= 2 -- the same target is O-suppressed against
  at least two independent anchor polarization lines.  Two O labels from anchors with
  parallel polarizations are NOT double-O.
  Reported per fixture: N_{O,1} = #{e : rank O(e) = 1},  N_{O,>=2} = #{e : rank O(e) >= 2}.

All arithmetic is exact (sympy over Q, Q(sqrt3) and Q(sqrt5)); no floats, no randomness.
"""

import itertools
from collections import Counter

import sympy as sp

R3 = sp.sqrt(3)

LABEL_NAMES = ("O", "E", "C", "T")


def proj(v, k):
    return v - (v.dot(k) / k.dot(k)) * k


def B(p, q, a, b):
    """Symmetric NSE triad interaction into k=p+q with a perp p, b perp q."""
    k = p + q
    return proj((a.dot(q)) * b + (b.dot(p)) * a, k)


def V(*xs):
    return sp.Matrix([sp.nsimplify(x) for x in xs])


def rank_of(vectors):
    if not vectors:
        return 0
    return sp.Matrix.hstack(*vectors).rank()


def classify(modes, in_cell):
    """modes: dict label -> (wavevector, amplitude); in_cell: predicate on |t|^2.

    Returns a list of per-target records.  Every contributing pair is an unordered pair of
    distinct-or-equal mode labels (combinations_with_replacement), matching one full local
    convolution generation of the registered web.
    """
    labels = list(modes)
    targets = {}
    for m, n in itertools.combinations_with_replacement(labels, 2):
        p, a = modes[m]
        q, b = modes[n]
        t = sp.simplify(p + q)
        if t == sp.zeros(3, 1):
            continue
        key = tuple(sp.nsimplify(x) for x in t)
        g = sp.simplify(B(p, q, a, b))
        aq = sp.simplify(a.dot(q))
        bp = sp.simplify(b.dot(p))
        eq = sp.simplify(p.dot(p) - q.dot(q)) == 0
        targets.setdefault(key, {"t": t, "contrib": []})["contrib"].append(
            {"m": m, "n": n, "g": g, "aq": aq, "bp": bp, "eqshell": eq}
        )

    out = []
    for key, d in targets.items():
        contrib = d["contrib"]
        net = sp.simplify(sum((c["g"] for c in contrib), sp.zeros(3, 1)))
        nonzero = [c for c in contrib if c["g"] != sp.zeros(3, 1)]
        rec = {"t": key, "n_contrib": len(contrib), "n_nonzero": len(nonzero)}
        if net != sp.zeros(3, 1):
            rec["status"] = "NOVELTY"
            out.append(rec)
            continue

        labels_set = set()
        # O(e): anchors whose polarization annihilates the partner wavevector.
        anchors = []
        for c in contrib:
            if c["aq"] == 0:
                labels_set.add("O")
                anchors.append(modes[c["m"]][1])
            if c["bp"] == 0:
                labels_set.add("O")
                anchors.append(modes[c["n"]][1])
        if any(c["eqshell"] for c in contrib):
            labels_set.add("E")
        if len(nonzero) >= 2:
            # C is an accounting label (exact multi-source cancellation), never a physical loss.
            labels_set.add("C")
        n2 = sp.simplify(d["t"].dot(d["t"]))
        if not in_cell(n2):
            labels_set.add("T")

        rec["status"] = "SUPPRESSED" if labels_set else "UNRESOLVED"
        rec["labels"] = [l for l in LABEL_NAMES if l in labels_set]
        rec["O_rank"] = rank_of(anchors)
        out.append(rec)
    return out


def summarize(name, recs):
    status = Counter(r["status"] for r in recs)
    labels = Counter(l for r in recs for l in r.get("labels", []))
    o_ranks = Counter(r["O_rank"] for r in recs if r["status"] == "SUPPRESSED")
    n_o1 = o_ranks.get(1, 0)
    n_o2 = sum(v for k, v in o_ranks.items() if k >= 2)
    print(f"{name}: targets={len(recs)} "
          f"SUPPRESSED={status.get('SUPPRESSED', 0)} NOVELTY={status.get('NOVELTY', 0)} "
          f"UNRESOLVED={status.get('UNRESOLVED', 0)}")
    print(f"  labels: O={labels.get('O', 0)} E={labels.get('E', 0)} "
          f"C={labels.get('C', 0)} T={labels.get('T', 0)}")
    print(f"  double-O: N_O,1={n_o1} N_O,>=2={n_o2} (rank of anchor polarizations per suppressed target)")
    return {"status": status, "labels": labels, "N_O1": n_o1, "N_O2": n_o2, "records": recs}


def find(recs, key):
    return [r for r in recs if r["t"] == key][0]


# ---------------------------------------------------------------------------
# Fixture W1 (copied exactly from check_ns_p2_multisource_cancellation.py):
# k=(1,0,0), two-shell N=2 exact cancellation.  Cell: |t|^2 <= 3.
# ---------------------------------------------------------------------------
W1 = [(V(1, 1, 0), V(0, -1, 0), V(-1, 1, -1), V(1, 0, 1)),
      (V(1, 0, 1), V(0, 0, -1), V(-1, 1, 1), V(2, 3, 0))]
modes_w1 = {}
for i, (p, q, a, b) in enumerate(W1):
    modes_w1[f"p{i}"] = (p, a)
    modes_w1[f"-p{i}"] = (-p, a)
    modes_w1[f"q{i}"] = (q, b)
    modes_w1[f"-q{i}"] = (-q, b)
S1 = summarize("W1 (cell |t|^2 <= 3)", classify(modes_w1, lambda n2: n2 <= 3))

# ---------------------------------------------------------------------------
# Fixture W2 (copied exactly from check_ns_p2_multisource_cancellation.py):
# k=(1,1,1), p_i = e_i, N=3 rank-2 exact cancellation.  Cell: |t|^2 <= 3.
# ---------------------------------------------------------------------------
k2 = V(1, 1, 1)
W2 = [(V(1, 0, 0), V(0, 66, -22), V(1, -1, 1)),
      (V(0, 1, 0), V(1, 0, 2), V(-2, 1, 2)),
      (V(0, 0, 1), V(3, 1, 0), V(-2, 2, 1))]
modes_w2 = {}
for i, (p, a, b) in enumerate(W2):
    q = k2 - p
    modes_w2[f"p{i}"] = (p, a)
    modes_w2[f"-p{i}"] = (-p, a)
    modes_w2[f"q{i}"] = (q, b)
    modes_w2[f"-q{i}"] = (-q, b)
S2 = summarize("W2 (cell |t|^2 <= 3)", classify(modes_w2, lambda n2: n2 <= 3))

# ---------------------------------------------------------------------------
# Fixture W3 point A: three equal-shell triads at k=(0,0,1), theta in {0, 2pi/3, 4pi/3},
# plus the retained k-mode.  Wavevectors and amplitudes are exact literals over Q(sqrt3)
# (lattice x = sqrt3/4 x_int, y = y_int/4, z = z_int/2).  Point A amplitude choice:
# A1 = 1, A2 = 0, B1 = 0, B2 = -1 for every triad; c = (1, 0, 0) at +-k.
# Cell: |t|^2 < 3, so every |t|^2 = 3 target (18 in this convolution, including the six outward
# generation-1 descendants p_i + k, q_i + k of the multisource note) is a registered exit.
# ---------------------------------------------------------------------------
W3A = {
    "p0":  (( R3 / 2, 0, sp.Rational(1, 2)),   (0, 1, 0)),
    "-p0": ((-R3 / 2, 0, -sp.Rational(1, 2)),  (0, 1, 0)),
    "q0":  ((-R3 / 2, 0, sp.Rational(1, 2)),   (sp.Rational(1, 2), 0, R3 / 2)),
    "-q0": (( R3 / 2, 0, -sp.Rational(1, 2)),  (sp.Rational(1, 2), 0, R3 / 2)),
    "p1":  ((-R3 / 4, sp.Rational(3, 4), sp.Rational(1, 2)),    (-R3 / 2, -sp.Rational(1, 2), 0)),
    "-p1": (( R3 / 4, -sp.Rational(3, 4), -sp.Rational(1, 2)),  (-R3 / 2, -sp.Rational(1, 2), 0)),
    "q1":  (( R3 / 4, -sp.Rational(3, 4), sp.Rational(1, 2)),   (-sp.Rational(1, 4), R3 / 4, R3 / 2)),
    "-q1": ((-R3 / 4, sp.Rational(3, 4), -sp.Rational(1, 2)),   (-sp.Rational(1, 4), R3 / 4, R3 / 2)),
    "p2":  ((-R3 / 4, -sp.Rational(3, 4), sp.Rational(1, 2)),   (R3 / 2, -sp.Rational(1, 2), 0)),
    "-p2": (( R3 / 4, sp.Rational(3, 4), -sp.Rational(1, 2)),   (R3 / 2, -sp.Rational(1, 2), 0)),
    "q2":  (( R3 / 4, sp.Rational(3, 4), sp.Rational(1, 2)),    (-sp.Rational(1, 4), -R3 / 4, R3 / 2)),
    "-q2": ((-R3 / 4, -sp.Rational(3, 4), -sp.Rational(1, 2)),  (-sp.Rational(1, 4), -R3 / 4, R3 / 2)),
    "k":   ((0, 0, 1),   (1, 0, 0)),
    "-k":  ((0, 0, -1),  (1, 0, 0)),
}
modes_w3 = {lbl: (sp.Matrix(kv), sp.Matrix(av)) for lbl, (kv, av) in W3A.items()}
for lbl, (kv, av) in modes_w3.items():
    assert sp.simplify(kv.dot(av)) == 0, lbl                      # transversality
    assert sp.simplify(kv.dot(kv)) == 1, lbl                      # all fourteen modes on the unit shell
S3 = summarize("W3 point A (cell |t|^2 < 3)", classify(modes_w3, lambda n2: n2 < 3))

# ---------------------------------------------------------------------------
# Fixture OT: orthogonal-turn generation-1 chain, time-honest web (EXACT FIXTURE / FINITE
# DIAGNOSTIC).  Similitude A = [[3,0,4],[4,0,-3],[0,5,0]] (A^T A = 25 I), seed p0 = (1,0,0),
# q0 = (2,4,0); p1 = p0 + q0 = (3,4,0), q1 = A q0 = (6,8,20).  Only the four modes the two
# selected steps need are registered (p2 = p1 + q1 not yet grown).  Polarizations fixed by the
# selected chain (NS_P2_ORTHOGONAL_TURN_ALLSCALE_ESCAPE.md sec. 5): p0 -> T0, q0 -> N0,
# p1 -> N0 (axis exchange T1 = N0), q1 -> N1, with N_j = p_j x q_j / |p_j x q_j|,
# T0 = N0 x p0 / |p0|.  Amplitudes H1-flat, |alpha_k| = 1 / |k|, real, so u(-m) = u(m); every
# amplitude vector is an exact literal over Q(sqrt5).  Declared cell: |t|^2 <= |q1|^2 = 500
# (the generator's own "OFF <= q1" split), so every target beyond the q1 shell is a registered
# exit (T).
#
# Provenance: generator script ot_chain_gen1_timehonest.py (polarization chain also in
# ot_chain_gen1_fullconv.py) of the internal attack repository, commit
# 83d8b5bf0ed15ab81033e0ce92af6e80c9596c95; the wavevectors, polarizations and H1-flat
# magnitudes are copied exactly from that script, and the public wavevector/turn geometry is
# the one certified by check_ns_p2_orthogonal_turn_allscale_escape.py.
# ---------------------------------------------------------------------------
R5 = sp.sqrt(5)
A_OT = sp.Matrix([[3, 0, 4], [4, 0, -3], [0, 5, 0]])
assert A_OT.T * A_OT == 25 * sp.eye(3)
p0_ot, q0_ot = V(1, 0, 0), V(2, 4, 0)
p1_ot = p0_ot + q0_ot
q1_ot = A_OT * q0_ot
assert p1_ot == A_OT * p0_ot
assert p1_ot == V(3, 4, 0) and q1_ot == V(6, 8, 20)
n0_ot = p0_ot.cross(q0_ot)
n1_ot = p1_ot.cross(q1_ot)
assert n0_ot.dot(n1_ot) == 0                                       # orthogonal turn
N0_ot = n0_ot / sp.sqrt(n0_ot.dot(n0_ot))
N1_ot = n1_ot / sp.sqrt(n1_ot.dot(n1_ot))
T0_ot = N0_ot.cross(p0_ot / sp.sqrt(p0_ot.dot(p0_ot)))
assert N0_ot == V(0, 0, 1) and T0_ot == V(0, 1, 0)
assert N1_ot == V(sp.Rational(4, 5), -sp.Rational(3, 5), 0)
assert sp.simplify(N1_ot.cross(p1_ot / sp.sqrt(p1_ot.dot(p1_ot))) - N0_ot) == sp.zeros(3, 1)   # T1 = N0
wv_ot = {"p0": p0_ot, "q0": q0_ot, "p1": p1_ot, "q1": q1_ot}
pol_ot = {"p0": T0_ot, "q0": N0_ot, "p1": N0_ot, "q1": N1_ot}
mag_ot = {k: 1 / sp.sqrt(wv_ot[k].dot(wv_ot[k])) for k in wv_ot}            # H1-flat |alpha| = 1/|k|
assert {str(sp.nsimplify(m)) for m in mag_ot.values()} == {"1", "sqrt(5)/10", "1/5", "sqrt(5)/50"}


def is_exact_vector(v):
    """Every entry algebraic and free of floating-point atoms."""
    return all(x.is_algebraic and not any(a.is_Float for a in sp.preorder_traversal(x)) for x in v)


modes_ot = {}
for k in wv_ot:
    amp = sp.Matrix([sp.nsimplify(x) for x in mag_ot[k] * pol_ot[k]])
    modes_ot[k] = (wv_ot[k], amp)
    modes_ot["-" + k] = (-wv_ot[k], amp)                                # real web: u(-m) = u(m)
for lbl, (kv, av) in modes_ot.items():
    assert sp.simplify(kv.dot(av)) == 0, lbl                            # k . u_k = 0 for every mode
    assert is_exact_vector(av), lbl                                     # exact amplitude, no floats
    assert av != sp.zeros(3, 1), lbl
assert modes_ot["q1"][1] == V(2 * R5 / 125, -3 * R5 / 250, 0)

# The interaction operator is the same Fourier-Leray form as the other checkers:
# B(p,q,a,b) = P_{p+q}[(a.q) b + (b.p) a], asserted symbolically.
_P = sp.Matrix(sp.symbols('P1:4', real=True)); _Q = sp.Matrix(sp.symbols('Q1:4', real=True))
_a = sp.Matrix(sp.symbols('a1:4', real=True)); _b = sp.Matrix(sp.symbols('b1:4', real=True))
_src = (_a.dot(_Q)) * _b + (_b.dot(_P)) * _a
_k = _P + _Q
assert sp.simplify(B(_P, _Q, _a, _b) - (_src - (_src.dot(_k) / _k.dot(_k)) * _k)) == sp.zeros(3, 1)

S4 = summarize("OT gen-1 time-honest, H1-flat (cell |t|^2 <= 500)", classify(modes_ot, lambda n2: n2 <= 500))

# Label output is independent of the amplitude normalization on this single-source web: the
# generator's second normalization (critical, |alpha|^2 = 1/|k|) gives identical labels.
modes_ot_crit = {}
for k in wv_ot:
    amp = sp.Matrix([sp.nsimplify(x) for x in (1 / sp.sqrt(sp.sqrt(wv_ot[k].dot(wv_ot[k])))) * pol_ot[k]])
    assert is_exact_vector(amp), k
    modes_ot_crit[k] = (wv_ot[k], amp)
    modes_ot_crit["-" + k] = (-wv_ot[k], amp)
S4c = summarize("OT gen-1 time-honest, critical (cell |t|^2 <= 500)", classify(modes_ot_crit, lambda n2: n2 <= 500))

# ---------------------------------------------------------------------------
# Deterministic exact assertions.
# ---------------------------------------------------------------------------
for S in (S1, S2, S3, S4, S4c):
    assert S["status"].get("UNRESOLVED", 0) == 0, S["status"]     # fail-closed: none unresolved

# W1: the k target (1,0,0) is C without E (two-shell cancellation, no equal-shell pair).
w1k = find(S1["records"], (1, 0, 0))
assert w1k["status"] == "SUPPRESSED" and "C" in w1k["labels"] and "E" not in w1k["labels"], w1k
assert w1k["n_contrib"] == 2 and w1k["n_nonzero"] == 2, w1k

# W3: the k target (0,0,1) is C and E (three equal-shell contributions cancel exactly).
w3k = find(S3["records"], (0, 0, 1))
assert w3k["status"] == "SUPPRESSED" and "C" in w3k["labels"] and "E" in w3k["labels"], w3k
assert w3k["n_contrib"] == 3 and w3k["n_nonzero"] == 3, w3k

# W2: the k target (1,1,1) is C without E (rank-2 cancellation of three unequal-shell pairs).
w2k = find(S2["records"], (1, 1, 1))
assert w2k["status"] == "SUPPRESSED" and "C" in w2k["labels"] and "E" not in w2k["labels"], w2k
assert w2k["n_contrib"] == 3 and w2k["n_nonzero"] == 3, w2k

# Per-fixture counts (exact, reproduced by this file; recorded in the paper tables).
assert len(S1["records"]) == 26 and S1["status"]["SUPPRESSED"] == 10
assert dict(S1["labels"]) == {"O": 8, "E": 8, "T": 8, "C": 2}
assert len(S2["records"]) == 56 and S2["status"]["SUPPRESSED"] == 14
assert dict(S2["labels"]) == {"O": 12, "E": 12, "T": 12, "C": 2}
assert len(S3["records"]) == 82 and S3["status"]["SUPPRESSED"] == 26
assert dict(S3["labels"]) == {"O": 16, "E": 26, "T": 16, "C": 2}

# Double-O rank counts.  W1/W2: every O-suppressed target is O-suppressed through exactly one
# polarization line (all N_{O,>=2} = 0).  W3 point A: the two double-O targets are +-k, where the
# three equal-shell contributions each have a_i . q_i = 0 with rank-2 (planar) anchor polarizations.
assert (S1["N_O1"], S1["N_O2"]) == (8, 0), (S1["N_O1"], S1["N_O2"])
assert (S2["N_O1"], S2["N_O2"]) == (12, 0), (S2["N_O1"], S2["N_O2"])
assert (S3["N_O1"], S3["N_O2"]) == (14, 2), (S3["N_O1"], S3["N_O2"])
double_o_w3 = sorted(str(r["t"]) for r in S3["records"] if r["status"] == "SUPPRESSED" and r["O_rank"] >= 2)
assert double_o_w3 == ["(0, 0, -1)", "(0, 0, 1)"], double_o_w3

# OT gen-1 time-honest web (EXACT FIXTURE / FINITE DIAGNOSTIC; not evidence that RSC passes globally).
assert len(S4["records"]) == 32 and S4["status"]["SUPPRESSED"] == 12 and S4["status"]["NOVELTY"] == 20
assert dict(S4["labels"]) == {"O": 12, "E": 8, "T": 2}                 # C = 0: no multi-source target
assert (S4["N_O1"], S4["N_O2"]) == (12, 0), (S4["N_O1"], S4["N_O2"])
# Every target of this web is single-source (one pair lands on it), so C cannot occur and every
# suppressed target is a projection zero of its only contribution.
assert all(r["n_contrib"] == 1 for r in S4["records"])
assert all(r["n_nonzero"] == 0 for r in S4["records"] if r["status"] == "SUPPRESSED")
# Selected forward channel p1 = p0 + q0 is productive (NOVELTY), as the chain requires.
assert find(S4["records"], (3, 4, 0))["status"] == "NOVELTY"
assert find(S4["records"], (9, 12, 20))["status"] == "NOVELTY"          # p2 = p1 + q1 target
# Tree-return target p0 = (1,0,0) from (-q0, p1) is O-suppressed: N0 . p1 = 0 and N0 . q0 = 0.
ot_p0 = find(S4["records"], (1, 0, 0))
assert ot_p0["status"] == "SUPPRESSED" and ot_p0["labels"] == ["O"], ot_p0
# Self-pair target 2 q1 = (12,16,40) is {O, E, T}: outside the cell |t|^2 <= 500.
ot_2q1 = find(S4["records"], (12, 16, 40))
assert ot_2q1["labels"] == ["O", "E", "T"], ot_2q1
# Normalization independence of the labels on this web.
assert dict(S4c["labels"]) == dict(S4["labels"]) and dict(S4c["status"]) == dict(S4["status"])
assert (S4c["N_O1"], S4c["N_O2"]) == (S4["N_O1"], S4["N_O2"])

print("W1 k target (1,0,0): C without E;  W2 k target (1,1,1): C without E;  W3 k target (0,0,1): C and E")
print("OT gen-1 time-honest web: UNRESOLVED=0, O12/E8/C0/T2, N_O,1/N_O,>=2 = 12/0 (EXACT FIXTURE / FINITE DIAGNOSTIC)")
print("C is an accounting label (exact multi-source cancellation), never a physical loss; Witness Soundness OPEN")
print("NS-P2 M3 SUPPRESSION LABELS PASS")
