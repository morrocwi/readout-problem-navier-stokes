# NS P2 — Recursive Suppression Charging Candidate Card

**Status:** OPEN THEOREM CANDIDATE / REUSE-FIRST DECOMPOSITION  
**Proposal id:** `PROP-P3-RECURSIVE-SUPPRESSION-CHARGING-01`  
**Parent route:** Standalone vNext §114.1 + A1 two-line reduction + OCSR / Witness Soundness frontier  
**Global FNW / OCSR / Witness Soundness / G4/G6/G7:** OPEN  
**Clay Navier–Stokes regularity:** OPEN

## 0. Reuse-first audit

Standing rule:

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

A Toledo lookup on 2026-09-12 found no canonical object named or equivalent to recursive suppression charging. This card therefore introduces no theorem claim; it records the exact missing global statement and decomposes it into already-typed branches.

Reused objects already on `main`:

- `PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01`;
- exact cancellation ledger;
- equal-shell direction lock;
- rank-2 polarization / plane-switch reductions;
- `PROP-P3-A1-TWO-LINE-ESCAPE-REDUCTION-01`;
- Standalone §114.1 no-silent-loss / null-web lineage discipline;
- OCSR + global cancellation compatibility + Witness Soundness as the canonical global frontier.

Pending input, not yet a premise of this branch:

- PR #59 Type-P shell-confinement / identity-loop fixtures. These may strengthen the equal-shell branch after merge, but this card does not depend on them.

NPSC finite sweeps may support falsification/calibration but are **not premises** of the global theorem candidate.

---

## 1. Suppression event and M3 label semantics

Let `e_j` be a future-relevant full-convolution descendant whose production is forced by the active local geometry but whose net realized response is suppressed at step `j`.

M3 is required to classify the suppression fail-closed by a **set of labels**, not by a single mutually-exclusive label:

\[
\boxed{
\mathsf L_j\subseteq
\{\mathrm O,\mathrm E,\mathrm C,\mathrm T\}
}
\]

with

```text
O = ORTHOGONALITY
E = EQUAL-SHELL NULLITY
C = EXACT MULTISOURCE CANCELLATION
T = TERMINAL / EXIT / NAMED DEFECT
```

The local meanings are:

\[
\mathrm O:\quad a\cdot q=0,
\]

\[
\mathrm E:\quad |q|=|p|,
\]

\[
\mathrm C:\quad
\sum_\alpha g_{\alpha,k}=0
\quad\text{with at least one }g_{\alpha,k}\neq0,
\]

while `T` records a declared terminal / exit / named-defect route.

A suppression that cannot be certified by any registered label is

```text
UNRESOLVED
```

and cannot be used in a promoted proof branch.

Important: `C` is a cancellation/constraint label only. It is **not** by itself a physical defect or payable loss.

---

## 2. Candidate global statement

The desired theorem candidate is:

\[
\boxed{
\begin{aligned}
&\text{compact productive recurrent two-line web}
\\
&+\text{zero registered defect / no terminal / no exit}
\\
&+\text{every forced descendant repeatedly suppressed and M3-resolved}
\\
&\Longrightarrow
\text{planar}
\ \vee\
\text{rank degeneration}
\ \vee\
\text{scale escape}
\ \vee\
\text{registered future-reader consequence}.
\end{aligned}
}
\tag{RSC}
\]

Status: **OPEN**.

This is the current A1 residue after the nonidentity Type-P reduction. A proof would fold A1 directly into OCSR / Witness Soundness rather than create a separate holonomy theorem.

---

## 3. Exact finite-alphabet reduction

Assume the left-hand side of (RSC) persists for infinitely many suppression steps and that no `T` label ever occurs.

Then every resolved event has a nonempty label-set

\[
\mathsf L_j\subseteq\{\mathrm O,\mathrm E,\mathrm C\},
\qquad
\mathsf L_j\neq\varnothing.
\]

Since only three atomic nonterminal labels exist, at least one atomic label occurs at infinitely many steps:

\[
\boxed{
\mathrm O\text{ infinitely often}
\ \vee\
\mathrm E\text{ infinitely often}
\ \vee\
\mathrm C\text{ infinitely often}.
}
\tag{RSC-1}
\]

This is only the infinite-pigeonhole reduction. It is exact, but it does **not** solve any of the three branches.

Because M3 labels are sets, mixed events such as `{O,E}` or `{E,C}` need no new global branch: they belong simultaneously to the corresponding atomic branches and therefore carry stronger, not weaker, constraints.

---

## 4. Three load-bearing branch obligations

A proof of (RSC) is reduced to the following three OPEN statements.

### RSC-O — repeated orthogonality charging

\[
\boxed{
\mathrm O\text{ infinitely often}
\Longrightarrow
\text{planar / rank-degenerate / exit / reader consequence}.
}
\]

Reusable local inputs:

- anchor-cross nullity;
- four-anchor no-silent-recruitment;
- shell-conditioned span and rank-2 polarization-plane rigidity.

The missing global step is to prevent the web from continually changing anchors / planes so that each new orthogonality constraint is discharged without accumulating a persistent lower-dimensional structure.

### RSC-E — repeated equal-shell charging

\[
\boxed{
\mathrm E\text{ infinitely often}
\Longrightarrow
\text{planar / rank-degenerate / scale escape / reader consequence}.
}
\]

Reusable inputs already on `main`:

- equal-shell direction lock;
- W3 / antipodal cancellation / cancellation-ladder exact families.

Pending strengthening after PR #59 merge:

- Type-P transport shell confinement.

The missing global step is to classify an arbitrary compact productive equal-shell recurrent web, not merely the existing exact families.

### RSC-C — repeated exact-cancellation charging

\[
\boxed{
\mathrm C\text{ infinitely often}
\Longrightarrow
\text{registered future-reader consequence / degeneration / exit}.
}
\]

Reusable inputs:

- exact cancellation ledger;
- W1/W2/W3 depth-1 audits;
- live cancellation-constraint interpretation;
- full-convolution descendants.

This is the branch most directly dependent on global multi-source cancellation compatibility + Witness Soundness. No implication

\[
C_k>0\Rightarrow\text{physical defect}
\]

is allowed.

---

## 5. Minimal dependency graph

```text
A1 two-line skeleton
      |
      v
forced descendant suppression
      |
      v
M3 fail-closed label-set
      |
      +--> T --------------------------> registered terminal / exit / defect
      |
      +--> O infinitely often --------> RSC-O  OPEN
      |
      +--> E infinitely often --------> RSC-E  OPEN
      |
      +--> C infinitely often --------> RSC-C  OPEN
                                          |
                                          v
                   OCSR + cancellation compatibility + Witness Soundness
                                          |
                                          v
                                     FNW / G6
```

Thus M3 is a classifier / falsifier and theorem interface. It is not itself the proof of (RSC).

---

## 6. Falsification protocol

The theorem candidate should be attacked before promotion.

Search for an exact compact productive recurrent web satisfying:

```text
no T event,
all forced descendants M3-resolved,
nonplanar,
rank >= 2,
no scale escape,
no future-reader consequence,
zero registered defect,
and an infinite / cyclic suppression history using only O/E/C labels.
```

An exact realized web of this form refutes (RSC) as stated.

Finite diagnostics such as W1-W3, orthogonal-turn generation-1, NPSC boxes, or T0-02 catalogues can falsify local variants and discover missing labels, but finite success cannot promote the global theorem.

---

## 7. Claim boundary

```text
M3 four-label / multi-label / UNRESOLVED interface                SPECIFIED
infinite nonterminal label extraction (RSC-1)                     DERIVED elementary
RSC-O repeated orthogonality charging                             OPEN
RSC-E repeated equal-shell charging                               OPEN
RSC-C repeated exact-cancellation charging                        OPEN
PROP-P3-RECURSIVE-SUPPRESSION-CHARGING-01                         OPEN THEOREM CANDIDATE
OCSR / global cancellation compatibility / Witness Soundness      OPEN
FNW / G6                                                          OPEN
G4 / G7                                                           OPEN
Clay Navier-Stokes regularity                                     OPEN
```

No theorem claim is promoted by this card.

---

## 8. Preferred next mathematical move

Do not invent a fifth suppression label unless an exact `UNRESOLVED` fixture forces it.

After M3 calibration on W1-W3 and orthogonal-turn generation-1, attack the three recurrent branches in order of leverage:

```text
1. RSC-O: use existing multi-anchor / rank-2 rigidity to seek a finite constraint-growth contradiction;
2. RSC-E: use equal-shell direction lock and compare with W3/T0-02 catalogues; add Type-P shell confinement only after PR #59 merge;
3. RSC-C: use exact cancellation ancestry to formulate the weakest Witness-Soundness-compatible charging statement.
```

The objective is not to prove that every suppression immediately loses energy. The objective is to prove that repeated suppression cannot remain compact, productive, nonplanar, reader-sufficient, and zero-defect indefinitely.
