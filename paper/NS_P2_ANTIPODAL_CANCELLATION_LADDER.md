# NS P2 — Exact Antipodal Cancellation Ladder

**Status:** NEW DERIVATION / PROPOSAL; exact symbolic restricted family  
**Global OCSR / Witness Soundness / cancellation compatibility:** OPEN  
**Clay Navier–Stokes regularity:** OPEN  
**Checker:** `reproduction/checks/check_ns_p2_antipodal_cancellation_ladder.py`

## 0. Reuse-first derivation

This note continues the existing cancellation/OCSR branch only. It reuses:

- the P2 symmetric projected NSE interaction;
- the exact cancellation ledger;
- the Genesis/Toledo no-silent-loss, sufficiency and lineage requirements;
- the exact antipodal cancellation/outward family already derived on the same branch.

A Toledo lookup for an existing antipodal-cancellation ladder object returned no match, so the result below is explicitly a new proposal rather than a Toledo theorem.

## 1. Strip geometry

Fix `K,P != 0`, the antipodal reality-coupled pair

\[
p=(0,P,0),\qquad -p=(0,-P,0),\qquad a=e_3,
\]

and for each integer `j` define

\[
q_j=(K,(2j+1)P,0).
\]

Choose a divergence-free polarization

\[
b_j=\left(-\frac{(2j+1)P}{K}c_j,\ c_j,\ z_j\right),
\]

so `q_j · b_j = 0` exactly.

## 2. Exact two-sided source rule

The reused bilinear interaction gives

\[
\boxed{B_{p,q_j}(a,b_j)=P c_j e_3}
\]

at

\[
s_{j+1}=p+q_j=(K,(2j+2)P,0),
\]

and

\[
\boxed{B_{-p,q_j}(a,b_j)=-P c_j e_3}
\]

at

\[
s_j=-p+q_j=(K,2jP,0).
\]

Thus every `q_j` feeds equal-and-opposite source strength into its lower and upper neighboring targets.

## 3. Constraint propagation

At an interior target `s_j`, two contributions meet:

\[
P c_{j-1}e_3-P c_j e_3.
\]

Exact cancellation is therefore equivalent to

\[
\boxed{c_j=c_{j-1}.}
\]

Hence a connected cancellation strip forces

\[
\boxed{c_m=c_{m+1}=\cdots=c_n.}
\]

This is precisely Generative Constraint Accumulation in an exact symbolic family: suppressing one target does not erase the source; it propagates a coefficient constraint to the next target.

## 4. Finite strips cannot be lossless

Take a finite strip

\[
q_m,q_{m+1},\ldots,q_n
\]

with all interior targets cancelled and with productive coefficient `c != 0`.

Then the lower boundary target `s_m` receives only

\[
-Pc\,e_3,
\]

and the upper boundary target `s_{n+1}` receives only

\[
+Pc\,e_3.
\]

Therefore

\[
\boxed{
\text{finite productive cancellation strip}
\Longrightarrow
\text{two nonzero boundary descendants}.
}
\]

To cancel either boundary, the web must recruit another `q` mode outside the strip.

## 5. Infinite recruitment is scale escape

The source scale is

\[
|q_j|^2=K^2+(2j+1)^2P^2.
\]

Thus

\[
|q_j|\to\infty\qquad\text{as }|j|\to\infty.
\]

So a bi-infinite productive strip that keeps cancelling every boundary cannot remain in a compact finite-relative-scale interior:

\[
\boxed{
\text{cancel forever in this family}
\Longrightarrow
\text{scale escape}.
}
\]

## 6. Proposed result

`PROP-P3-ANTIPODAL-CANCEL-LADDER-01` — **NEW DERIVATION / PROPOSAL; exact symbolic PASS**.

Restricted-family statement:

```text
Within the declared antipodal strip family, exact cancellation at every
interior target forces constant productive source coefficient along the
strip. Every finite productive strip has two uncancelled boundary
descendants; extending the strip to cancel those descendants forces
unbounded wavevector magnitude. Hence no nonzero compact lossless recurrent
cancellation strip exists in this family.
```

## 7. What this advances

This is stronger than a single antipodal witness:

- it holds at arbitrary finite depth;
- it turns repeated cancellation into an exact recurrence on the constraint `c_j`;
- it proves a clean dichotomy in this family:

```text
finite strip -> outward/boundary novelty
infinite strip -> scale escape
```

This is an exact restricted-family instance of the desired OCSR / cancellation-compatibility mechanism.

It does **not** prove global OCSR because a general web can recruit modes outside this strip geometry and attempt cross-family cancellation.

## 8. Next missing piece

The reusable next target is now sharply defined:

```text
Can a mode outside the antipodal strip cancel a strip boundary descendant
without creating either another larger-scale descendant or an additional
independent cancellation constraint?
```

That is the first genuinely cross-family cancellation question. No new global architecture is needed.
