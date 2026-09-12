# NS P2 — Four-Anchor No-Silent-Recruitment Corollary

**Status:** NEW DERIVATION / PROPOSAL; exact finite corollary  
**Parent:** `PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01`  
**Global OCSR / Witness Soundness / cancellation compatibility:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_multi_anchor_suppression.py`

## 0. Reuse-first path

This note applies the system rule

```text
Toledo lookup -> Genesis compatibility -> reuse existing object -> derive only the missing piece -> mark PROPOSAL
```

No new architecture is introduced.

Reused objects:

- the exact local nullity classification from `PROP-P3-GENERAL-ANCHOR-CROSS-NULLITY-01`;
- the existing full-convolution semantics;
- Genesis retention/sufficiency discipline: a cross interaction may be absent only by an exact registered algebraic reason, not silent deletion.

A Toledo lookup for a multi-anchor suppression theorem returned no matching object. The statement below is therefore a proposal.

## 1. Four retained anchors

Let

\[
(p_i,a_i),\qquad i=1,2,3,4,
\]

be four retained anchor mode/polarization pairs with

\[
p_i\neq0,\qquad a_i\neq0,\qquad a_i\cdot p_i=0.
\]

Assume their shell radii are pairwise distinct:

\[
\boxed{|p_i|\neq |p_j|\quad(i\neq j).}
\tag{MA-1}
\]

Assume also that every triple of anchor polarizations is linearly independent:

\[
\boxed{
\operatorname{rank}(a_i,a_j,a_k)=3
\quad\text{for every distinct }i,j,k.
}
\tag{MA-2}
\]

Now take a nonzero recruited source mode

\[
q\neq0
\]

with one nonzero polarization

\[
b\in q^\perp,\qquad b\neq0,
\]

and assume

\[
p_i+q\neq0
\]

for every anchor.

## 2. Suppressing one anchor costs one exact constraint

By the reused general anchor-cross nullity theorem, if

\[
\mathcal B_{p_i,q}(a_i,b)=0,
\]

then necessarily

\[
\boxed{
 a_i\cdot q=0
 \quad\vee\quad
 |q|=|p_i|.
}
\tag{MA-3}
\]

Thus being cross-silent to each retained anchor is not free; it requires one exceptional-locus condition per anchor.

## 3. Pairwise-distinct shells allow at most one shell escape

Because the four numbers

\[
|p_1|,|p_2|,|p_3|,|p_4|
\]

are pairwise distinct, one fixed `|q|` can equal at most one of them.

Therefore if `q` suppresses all four anchors, at least three of the four conditions (MA-3) must use the orthogonality branch:

\[
\boxed{
 a_i\cdot q=0
}
\]

for at least three distinct indices.

## 4. Three independent orthogonality constraints force q=0

By (MA-2), those three corresponding polarization vectors span `R^3`. Hence the only vector orthogonal to all three is

\[
q=0.
\]

This contradicts the assumption that the recruited source mode is nonzero.

Therefore:

\[
\boxed{
\max_{1\le i\le4}
\|\mathcal B_{p_i,q}(a_i,b)\|>0.
}
\tag{MA-4}
\]

In words: **a nonzero recruited mode cannot be simultaneously cross-silent to four shell-distinct retained anchors whose polarizations are in triple-wise general position.**

## 5. Equivalent degeneracy form

Taking the contrapositive of the hypotheses gives the form most useful for OCSR:

\[
\boxed{
\begin{aligned}
&\mathcal B_{p_i,q}(a_i,b)=0\quad\forall i=1,2,3,4
\\
&\Longrightarrow
\Bigl(\exists i\neq j:\ |p_i|=|p_j|\Bigr)
\ \vee\ 
\Bigl(\exists i,j,k:\ \operatorname{rank}(a_i,a_j,a_k)<3\Bigr)
\ \vee\ q=0.
\end{aligned}
}
\tag{MA-5}
\]

Since `q=0` is excluded for a recruited mode, complete four-anchor silence forces either

```text
shell collision
OR
polarization-rank degeneration.
```

This is an exact finite instance of Generative Constraint Accumulation: once enough independent retained anchors exist, a new source cannot remain silent without driving the web onto a lower-dimensional exceptional set.

## 6. Non-vacuity family

The checker records the exact rational anchor family

\[
p_1=(1,0,0),\quad a_1=(0,1,0),
\]

\[
p_2=(0,2,0),\quad a_2=(0,0,1),
\]

\[
p_3=(0,0,3),\quad a_3=(1,0,0),
\]

\[
p_4=(4,4,0),\quad a_4=(1,-1,1).
\]

The squared radii are

\[
1,4,9,32,
\]

and every polarization triple has nonzero determinant. Hence the hypotheses are nonempty and exact.

## 7. Proposed result

`PROP-P3-MULTI-ANCHOR-SUPPRESSION-01` — **NEW DERIVATION / PROPOSAL; exact finite PASS**.

Bounded statement:

```text
For four retained anchors with pairwise-distinct shell radii and with every
triple of anchor polarizations linearly independent, no nonzero recruited
mode/polarization can suppress all four anchor-cross interactions. Therefore
complete four-anchor silence forces shell collision or polarization-rank
degeneration (apart from the excluded zero mode).
```

## 8. What this advances

The previous one-anchor theorem classified the exceptional loci for a single suppressed cross interaction.

This corollary shows those exceptions **cannot be chosen independently forever** once four sufficiently generic retained anchors coexist:

\[
\text{four-anchor silence}
\Longrightarrow
\text{degenerate shell/polarization geometry}.
\]

That is qualitatively closer to OCSR than a single outward witness because it converts repeated suppression into a finite degeneracy certificate.

## 9. What remains OPEN

This does not yet prove OCSR because a recurrent web may avoid the four-anchor hypotheses by:

- repeatedly reusing equal shell radii;
- keeping polarization rank at most two;
- failing to retain four anchors simultaneously in the required reader-sufficient state;
- routing activity through another declared boundary/exit mechanism.

Therefore still OPEN:

- rigidity of the shell-collision branch;
- rigidity of the polarization-rank-degenerate branch;
- proof that a compact productive recurrent interior web necessarily reaches a four-anchor general-position configuration or one of those degeneracies;
- global multi-source cancellation compatibility;
- OCSR / Witness Soundness globally;
- G6/G7;
- Clay Navier–Stokes regularity.

## 10. Next reuse-first target

The next work should **not** invent another global object. It should attack the two exceptional branches in (MA-5) using existing results:

```text
A. shell collision -> reuse equal-shell direction lock + cancellation ledger
B. polarization rank <= 2 -> reuse planar/dispersion/orthogonal-web machinery
```

If both branches can be shown to lead to registered degeneration, novelty, or scale exit, the local OCSR route will tighten substantially without changing architecture.
