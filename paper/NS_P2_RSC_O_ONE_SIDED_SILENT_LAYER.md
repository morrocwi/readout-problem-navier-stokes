# NS P2 — RSC-O One-Sided Persistence Gives a Silent Recruit Layer

**Status:** NEW DERIVATION / PROPOSAL; exact local reduction  
**Proposal id:** `PROP-P3-RSC-O-ONE-SIDED-SILENT-LAYER-01` — not yet in Toledo  
**Parent route:** merged PR #63 `PROP-P3-RSC-O-ALTERNATION-TRANSFER-01` (ALT-1) / merged PR #60 RSC-O  
**Global RSC-O / RSC-E / RSC-C / OCSR / Witness Soundness / G6/G7:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_rsc_o_one_sided_silent_layer.py`  
**Date:** 2026-09-13

## 0. Reuse-first audit

Standing rule:

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

A Toledo lookup (registry, canonical map, the NS P2 critical-quotient proposals) found no canonical
object for the one-sided single-O recruit layer below.

Reused objects (not re-derived):

- **(ALT-1)** of `paper/NS_P2_RSC_O_ALTERNATION_TRANSFER.md` (`PROP-P3-RSC-O-ALTERNATION-TRANSFER-01`,
  PR #63, merged at `936225f7`): a genuine nonparallel O-suppressed recruit `(q,b)` of the anchor
  `(p,a)` satisfies `b·p = 0`, `b·q = 0`, hence `[b] = [a]`.
- **RSC-O two-anchor planarity** (`PROP-P3-RSC-O-TWO-ANCHOR-PLANARITY-01`, PR #60): the
  anchor/recruit convention — an anchor is O-silent to a recruit through `a·q = 0`.
- the exact projected NSE bilinear interaction `B_{p,q}(a,b) = P_{p+q}[(a·q) b + (b·p) a]`
  (the same operator as every other checker on `main`);
- the **cancellation ledger** (`PROP-P2-CANCELLATION-LEDGER-01`): exact multi-source cancellation
  is an accounting entry, never a physical loss;
- the **M3 labels** `O / E / C / T` and `UNRESOLVED` of `paper/NS_P2_M3_SUPPRESSION_LABELS.md`
  (`PROP-P3-M3-SUPPRESSION-LABELS-01`, PR #62), used only as names for the branches of the
  reduction in §4.

No new global architecture is introduced.

---

## 1. Setting — one-sided O_+ persistence

Fix the two distinct recurrent projective polarization classes `[a_+]`, `[a_-]` of the A1
two-line skeleton. PR #63 split the RSC-O frontier into

```text
A. infinitely many genuine O-line switches   -> transferred to RSC-E / RSC-C (ALT-4);
B. eventually one-sided single-O persistence -> this note;
C. parallel anchor/recruit degeneracy        -> OPEN;
D. double-O events                           -> two-anchor planarity certificate (local).
```

**One-sided O_+ persistence** means: from some generation on, every O-labelled recruit
`(q_j, b_j)`, `j = 1, 2, …`, is a genuine nonparallel single-O event against the `[a_+]` anchor
line:

\[
a_+\cdot q_j = 0,\qquad b_j\cdot q_j = 0,\qquad p_j\times q_j\neq 0,
\qquad \mathcal B_{p_j,q_j}(a_+,b_j)=0 .
\]

By (ALT-1), each such recruit copies the suppressed anchor line:

\[
q_j\in a_+^{\perp},\qquad [b_j]=[a_+]\qquad\text{for every }j .
\tag{OS-0}
\]

Nothing else is assumed about the recruits: their shells, their mutual angles inside the plane
`a_+^\perp`, and their amplitudes are free.

---

## 2. The recruit layer is quadratically silent to itself

Take any two recruits `(q_i,b_i)`, `(q_j,b_j)` of the layer (including `i = j`). Write
`b_i = s_i a_+`, `b_j = s_j a_+` by (OS-0). Since `q_i, q_j \in a_+^\perp`,

\[
b_i\cdot q_j = s_i\,(a_+\cdot q_j) = 0,
\qquad
b_j\cdot q_i = s_j\,(a_+\cdot q_i) = 0 .
\tag{OS-1}
\]

Therefore the unprojected source of the recruit–recruit interaction is already zero and

\[
\boxed{
\mathcal B_{q_i,q_j}(b_i,b_j)
=P_{q_i+q_j}\big[(b_i\cdot q_j)\,b_j+(b_j\cdot q_i)\,b_i\big]
=0
\qquad\text{for all } i,j .
}
\tag{OS-2}
\]

(OS-2) holds identically — for every pair of recruit shells, every pair of directions inside
`a_+^\perp`, every amplitude, and whether or not `q_i + q_j` lies in any cell. The checker
proves it symbolically for a generic anchor polarization `n = a_+` and two recruit wavevectors
parametrised by the orthogonal pair `v_1 = (n_2, −n_1, 0)`, `v_2 = (n_1 n_3, n_2 n_3, −(n_1² + n_2²))`,
which is a basis of `n^\perp` whenever `(n_1, n_2) ≠ (0, 0)`; the excluded axis case `n ∥ e_3` is
covered by the first rational fixture (`a_+ = (0,0,1)`), and in any case (OS-1)–(OS-2) use only
`a_+·q_i = a_+·q_j = 0`, never the parametrisation. Two explicit rational fixtures confirm (OS-2).

**Reading.** The recruit layer has **no recruit–recruit quadratic productivity**: it is a
**2D3C-like passive layer with respect to internal recruit–recruit interactions**. All recruit
wavevectors lie in one plane `a_+^\perp` and all recruit polarizations lie on the one normal line
`[a_+]` — exactly the Fourier-side signature of a plane-supported flow whose in-plane velocity is
zero and whose normal component is a passively advected scalar. This is **not** a full 2D3C
branch: the layer is silent only to itself. Interactions between a recruit and the `O_-` anchor
line, the retained backbone / core modes, or any mode outside the layer are not constrained by
(OS-2) and may stay active.

**Non-vacuity.** The control in the checker takes the same recruit wavevectors and moves one
recruit polarization off the line `[a_+]` (still transversal): the interaction becomes nonzero.
So (OS-2) is a consequence of the line copy (ALT-1), not of the wavevector planarity alone.

---

## 3. Reduction — persistent productivity must cross the layer/core interface

Under one-sided `O_+` persistence, the productive quadratic couplings of the web split as

```text
recruit x recruit      : identically zero          (OS-2)
recruit x core / O_-   : unconstrained here
core    x core         : unconstrained here
```

where "core" denotes every retained mode outside the silent layer (the `[a_-]` anchor line,
the backbone, and any recruit that is not a genuine single-`O_+` event). Hence:

\[
\boxed{
\text{one-sided } O_+ \text{ persistence}
\ \Longrightarrow\
\text{all persistent productivity crosses the layer/core interface.}
}
\tag{OS-3}
\]

Every productive descendant of the layer is sourced by a pair with at least one factor in the
core. The one-sided O-branch therefore cannot sustain itself as a self-contained productive
sub-web; a zero-novelty one-sided history needs the core as a permanent partner.

This is a reduction only. It does not say that the interface productivity is bounded, that it
forces a scale escape, or that it charges any defect.

---

## 4. Next target box (OPEN)

The surviving question after (OS-3) is the interface itself:

```text
passive O_+ layer  +  active O_- core
   ==>  double-O  v  E  v  C  v  novelty / exit         (OPEN)
```

That is: for a compact, productive, full-convolution-closed, zero-novelty one-sided history, does
every interface descendant of a layer recruit against the `O_-` core become either a double-O
event (then the two-anchor planarity certificate of PR #60 applies locally), an equal-shell event
(`E`, RSC-E), an exact multi-source cancellation (`C`, RSC-C, accounting only), or registered
novelty / exit? No answer is claimed here. The M3 labels are used only as names for the branches
of this box.

---

## 5. Proposed result

`PROP-P3-RSC-O-ONE-SIDED-SILENT-LAYER-01` — **NEW DERIVATION / PROPOSAL; exact local reduction**.

Bounded statement:

```text
Under one-sided O_+ persistence every recruit satisfies q_j in a_+^perp and
[b_j] = [a_+] (ALT-1, PR #63).  Hence for all i, j:  b_i.q_j = b_j.q_i = 0 and
therefore B_{q_i,q_j}(b_i,b_j) = 0: the recruit layer has no recruit-recruit
quadratic productivity.  It is a 2D3C-like passive layer with respect to
internal recruit-recruit interactions, not a full 2D3C branch: interactions
with the O_- anchor / core may stay active.  Consequently all persistent
productivity must cross the layer/core interface.
```

---

## 6. Claim boundary

```text
recruit-recruit silence under one-sided O_+ persistence (OS-2)      DERIVED exact / proposal
all persistent productivity crosses the layer/core interface (OS-3) DERIVED reduction / proposal
passive O_+ layer + active O_- core => double-O v E v C v
                                        novelty/exit                  OPEN (next target box)
RSC-O branch A (infinite genuine O-line switching)                  transferred to RSC-E / RSC-C (PR #63)
RSC-O branch B (one-sided single-O persistence)                     this reduction only; not closed
RSC-O branch C (parallel anchor/recruit degeneracy)                 OPEN
RSC-O branch D (double-O events)                                    local planarity certificate only (PR #60)
RSC-O global                                                     OPEN
RSC-E / RSC-C                                                    OPEN
OCSR / Witness Soundness / G6/G7                                 OPEN
Clay Navier-Stokes regularity                                    OPEN
```

No cancellation label is promoted to physical loss. The phrase "2D3C-like" is a description of
the layer's internal interaction algebra only; no classical 2D regularity theorem is invoked for
the web, because the layer/core interface is not silenced.

---

## 7. Status

```text
PROP-P3-RSC-O-ONE-SIDED-SILENT-LAYER-01  symbolic identity (OS-2)   PASS (exact; not yet in Toledo)
two rational fixtures, B == 0 componentwise                       PASS
control: off-line recruit polarization gives B != 0               PASS
```
