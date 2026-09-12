# NS P2 — RSC-O Single-O Alternation Transfer

**Status:** NEW DERIVATION / PROPOSAL; exact local reduction  
**Proposal id:** `PROP-P3-RSC-O-ALTERNATION-TRANSFER-01`  
**Parent route:** merged PR #60 recursive suppression charging / RSC-O  
**Global RSC-O / RSC-E / RSC-C / OCSR / Witness Soundness / G6/G7:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_rsc_o_alternation_transfer.py`

## 0. Reuse-first audit

Standing rule:

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

A Toledo lookup found no canonical object for the specific single-O alternation transfer below.

Reused objects:

- exact projected NSE bilinear interaction `B`;
- `PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01`;
- merged PR #60 `PROP-P3-RSC-O-TWO-ANCHOR-PLANARITY-01`;
- the A1 two-line skeleton and recursive-suppression alphabet;
- full-convolution semantics and the cancellation ledger.

No new global architecture is introduced.

---

## 1. One genuine nonparallel single-O event copies its polarization line

Fix one retained anchor `(p,a)` and one recruited mode/polarization `(q,b)` with

\[
a\cdot p=0,\qquad b\cdot q=0,
\]

and suppose the interaction is suppressed through the orthogonality branch

\[
a\cdot q=0,
\qquad
\mathcal B_{p,q}(a,b)=0.
\]

Because `a` is perpendicular to both `p` and `q`, it is also perpendicular to `k=p+q`. Hence Leray projection does not change the `a` direction and

\[
\mathcal B_{p,q}(a,b)=(b\cdot p)a.
\]

Therefore exact suppression gives

\[
b\cdot p=0.
\]

Together with `b\cdot q=0`, if

\[
p\times q\neq0,
\]

then `p^\perp\cap q^\perp` is one-dimensional. Since `a` lies in that intersection and `a\neq0`, every nonzero suppressed recruited polarization satisfies

\[
\boxed{[b]=[a].}
\tag{ALT-1}
\]

So a genuine nonparallel single-O event does not create a new projective polarization class: it copies the suppressed anchor line.

The parallel branch `p x q = 0` is kept as a declared degeneracy and is not absorbed into this lemma.

---

## 2. Alternating single-O events

Let `[a_+]` and `[a_-]` be the two distinct recurrent projective polarization classes of the A1 two-line skeleton.

Consider two consecutive genuine single-O recruits `(q,b)` and `(r,d)` such that

\[
a_+\cdot q=0,\qquad a_-\cdot q\neq0,
\]

\[
a_-\cdot r=0,\qquad a_+\cdot r\neq0.
\]

Assume their corresponding anchor/recruit pairs are nonparallel, so by (ALT-1)

\[
[b]=[a_+],\qquad[d]=[a_-].
\]

In particular the second genuine single-O condition gives

\[
b\cdot r\neq0.
\]

Now apply the reused general anchor-cross nullity theorem to the cross interaction

\[
\mathcal B_{q,r}(b,d).
\]

For anchor `(q,b)` and source mode `r`, the only ways that a nonzero source polarization can lie in the kernel are

\[
b\cdot r=0
\quad\vee\quad
|r|=|q|.
\]

The first alternative is excluded by genuine alternation. Hence

\[
\boxed{
\mathcal B_{q,r}(b,d)=0
\Longrightarrow
|q|=|r|.
}
\tag{ALT-2}
\]

Thus exact individual nullity of the cross descendant forces an equal-shell charge.

---

## 3. Full-convolution event consequence

Full convolution contains the cross target

\[
k=q+r.
\]

For a genuine alternating pair, `r=-q` is impossible because that would make the two O-conditions coincide and violate the declared single-O inequalities. Hence `k!=0`.

There are then only the following fail-closed possibilities for the cross target:

1. the individual cross contribution is nonzero and survives as registered novelty / reader-relevant response;
2. the individual cross contribution vanishes, in which case (ALT-2) forces the M3 `E` label;
3. the individual cross contribution is nonzero but the net target is suppressed by other nonzero contributions, in which case the cancellation ledger records `C`;
4. the target is registered terminal / exit / named defect (`T`);
5. a prerequisite anchor/recruit pair is parallel, which is a declared geometric degeneracy outside the present nonparallel lemma.

Therefore a genuine nonparallel single-O alternation cannot remain an `O`-only zero-novelty mechanism:

\[
\boxed{
O_+\to O_-
\Longrightarrow
\text{novelty/response}
\ \vee\ E
\ \vee\ C
\ \vee\ T
\ \vee\ \text{parallel degeneracy}.
}
\tag{ALT-3}
\]

The same statement holds with `+` and `-` exchanged.

---

## 4. Recurrent reduction

Consider an infinite fixed-two-line suppression history in which:

- every O-labelled event is genuine single-O;
- the active O-line alternates infinitely often between `[a_+]` and `[a_-]`;
- the relevant anchor/recruit pairs are nonparallel;
- no registered novelty/reader consequence survives;
- no `T` event occurs.

Then every genuine change of O-line creates an adjacent alternating pair. By (ALT-3), each such pair must pay `E` or `C`.

Hence if the O-line switches infinitely often,

\[
\boxed{
E\text{ occurs infinitely often}
\ \vee\
C\text{ occurs infinitely often}.
}
\tag{ALT-4}
\]

This transfers the infinite genuine-alternation subbranch of `RSC-O` into the already-declared `RSC-E` or `RSC-C` obligations.

This does **not** close global `RSC-O`. Surviving O-residues include, for example:

- eventually one-sided single-O histories with only finitely many line switches;
- parallel anchor/recruit degeneracies;
- histories where the fixed-two-line hypothesis itself fails through a registered reanchor / rank transition;
- unresolved event realization.

---

## 5. Proposed result

`PROP-P3-RSC-O-ALTERNATION-TRANSFER-01` — **NEW DERIVATION / PROPOSAL; exact local/recurrent reduction**.

Bounded statement:

```text
For a fixed two-line A1 skeleton, a nonparallel O-suppressed recruit copies the
suppressed anchor's projective polarization line. Therefore two consecutive
genuine single-O recruits attached to opposite fixed lines have a nonzero
cross interaction unless the two recruited wavevectors are equal-shell.
Under full convolution, a zero-novelty alternating O history must therefore
pay EQUAL-SHELL, exact multisource CANCELLATION, T/E/D, or a declared parallel
degeneracy at every genuine line switch. Infinite genuine alternation with no
novelty and no T reduces to RSC-E or RSC-C.
```

---

## 6. Claim boundary

```text
single-O polarization-line copy, nonparallel branch              DERIVED exact / proposal
alternating-pair cross-null => equal-shell                       DERIVED exact / proposal
infinite genuine O-line switching => E infinitely often OR
                                      C infinitely often         DERIVED reduction / proposal
parallel anchor/recruit branch                                   OPEN / separate degeneracy
one-sided infinite single-O persistence                          OPEN
RSC-O global                                                     OPEN
RSC-E / RSC-C                                                    OPEN
OCSR / Witness Soundness / G6/G7                                 OPEN
Clay Navier-Stokes regularity                                    OPEN
```

No cancellation label is promoted to physical loss.

---

## 7. Next target

The RSC-O frontier is now split into:

```text
A. infinitely many genuine O-line switches
      -> transferred to RSC-E or RSC-C by this proposal;

B. eventually one-sided single-O persistence
      -> next exact target;

C. parallel anchor/recruit degeneracy
      -> classify as scale-ray / rank / terminal structure;

D. double-O events
      -> reuse merged two-anchor planarity certificate.
```

The preferred next local question is whether an eventually one-sided single-O
history can remain compact, productive, full-convolution closed and zero-novelty
without forcing either double-O, equal-shell locking, cancellation ancestry or
scale escape.
