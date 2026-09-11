# NS P2 — High–High absorption as a continuum semantic adapter

**Date:** 2026-09-11  
**Tracker:** issue #41.  
**Status:** adapter specification / audit target.  
**Claim boundary:** no global-regularity claim. The external source is a non-peer-reviewed preprint and is treated only as a candidate semantic adapter until independently audited.

## 1. Architectural rule

The finite-first programme does **not** require continuum mathematics to disappear from the final proof architecture. It requires continuum statements to be isolated behind an explicit adapter boundary rather than silently imported into the finite core.

The intended separation is

```text
FINITE-NATIVE CORE
  exact Galerkin/triad algebra
  finite shell/time certificates
  rational PASS/HOLD margins
  finite extension / weighted-tail proofs
          |
          | uniform translation theorem
          v
CONTINUUM SEMANTIC ADAPTER
  shellwise High–High absorption
  weighted Sobolev closure
  continuation theorem
          |
          v
GLOBAL REGULARITY CONSEQUENCE
```

The Clay-strength work is on the first arrow. A continuum theorem may close the second arrow if its hypotheses have already been established by the finite-native system without circularly assuming the desired regularity.

## 2. External candidate adapter

A directly aligned candidate is:

Shin-ichi Inage, *Conditional Regularity of the Three-Dimensional Navier–Stokes Equations via High–High Triadic Absorption*, Preprints.org, version 1 posted 20 March 2026, DOI `10.20944/preprints202603.1591.v1`.

The source explicitly presents its main regularity theorem as **conditional**, not as an unconditional solution of the 3D Navier–Stokes global-regularity problem. The posted version is a preprint and is not peer-reviewed.

The relevant continuum condition is schematically

\[
T_j^{HH}(t)\le \eta V_j(t)+\rho_j(t),
\qquad 0<\eta<1,
\]

with a Sobolev-weighted summability condition on the shell remainder `rho_j`. Under its internal Low–Low / Low–High estimates, the paper derives a closed weighted Sobolev inequality and then invokes continuation for `s>5/2`.

This programme does **not** adopt the later motivational/dynamical claims of that preprint as proved inputs. Only a theorem that survives independent audit may be used as an adapter.

## 3. Finite certificate language

For a finite shell/time cell `(j,I)`, define a proposed adapter certificate record

\[
\mathcal A_{j,I}=
(j,I,\eta,T^+_{j,I},V^-_{j,I},\rho^+_{j,I},w_j),
\]

where all numeric fields are rational and

- `T^+` is a certified upper bound on the High–High transfer relevant to the adapter convention;
- `V^-` is a certified lower bound on the viscous shell quantity;
- `rho^+ >= 0` is the declared remainder budget;
- `eta` is a rational number with `0 <= eta < 1`;
- `w_j` is the Sobolev shell weight used by the target adapter.

The local exact verifier accepts only if

\[
T^+_{j,I}\le \eta V^-_{j,I}+\rho^+_{j,I}.
\]

If the certified bounds are sound, this finite inequality implies the desired absorption inequality on that shell/time cell.

The checker is deliberately one-sided and fail-closed. Missing or non-strict evidence returns HOLD; it never infers absorption from numerical appearance.

## 4. Finite weighted-remainder verifier

For a finite shell range `j0 <= j <= J`, a finite certificate may also verify

\[
R_{\le J}:=\sum_{j=j_0}^{J} w_j\rho^+_j\le R^+_{\le J}
\]

by exact rational arithmetic.

This is still only a finite prefix. To feed a continuum adapter one additionally needs a certified tail theorem

\[
\sum_{j>J}w_j\rho_j\le R^+_{>J}
\]

or another uniform summability theorem. The adapter is not allowed to replace this missing all-shell step.

## 5. Translation obligations

Before the external theorem can be used, the programme must prove all of the following translations.

### A. Convention map

Map the repository's Fourier/Galerkin modes and shell grouping to the adapter's dyadic shell convention. This includes normalization, signs, energy definitions, Leray projection convention, and the precise definition of `T_j^{HH}` and `V_j`.

### B. Finite transfer enclosure

Construct a finite exact/interval certificate whose `T^+_{j,I}` really bounds the continuum-adapter High–High shell transfer for the represented finite state/time cell.

### C. Viscous lower enclosure

Construct a certified `V^-_{j,I}` in the same normalization.

### D. Time coverage

A finite list of time cells must cover the target time interval, or an analytic interpolation/variation modulus must bridge the gaps.

### E. All-shell extension

Finite shell verification must be extended to every shell required by the adapter using a summable tail theorem, not by enumerating a large but finite maximum shell.

### F. Remainder summability

The weighted `rho_j` remainder must satisfy the adapter's global summability hypothesis by an independent finite/uniform proof.

Only after A–F are established does the continuum conditional theorem become a legitimate semantic adapter.

## 6. Non-vacuity audit

The following do **not** count as successful finite-to-adapter bridges:

1. defining `rho_j` to be the exact positive defect `max(T_j^{HH}-eta V_j,0)` and then assuming its Sobolev-weighted sum is finite without a new bound;
2. assuming a uniform `H^s`, `s>5/2`, bound in order to prove the weighted remainder summability needed to recover that same regularity;
3. checking finitely many shells and silently replacing `j<=J` by `j<infinity`;
4. using an unvalidated simulation of `T_j^{HH}` as a certificate;
5. relying on the external preprint's heuristic phase/coherence discussion as if it proved the absorption hypothesis unconditionally.

Any such route is HOLD under the programme's non-vacuity rule.

## 7. Relationship to the current P2 tail split

`paper/NS_FUB_A1_STOKES_NONLINEAR_TAIL_SPLIT.md` isolates

```text
linear Stokes memory       -> explicit high-frequency tail gain
old nonlinear history      -> explicit gain when a positive time gap exists
recent nonlinear transfer  -> OPEN load-bearing term
```

The High–High adapter suggests a sharper target for that recent term: rather than bounding it only as an undifferentiated Duhamel remainder, decompose recent nonlinear transfer into shellwise interaction classes and certify that the dangerous High–High component is absorbed by viscosity up to a weighted summable remainder.

Thus the two lines connect as

```text
Stokes/old-history explicit tail control
+ finite High–High absorption certificates for recent transfer
+ all-shell weighted remainder theorem
        |
        v
external continuum absorption adapter
        |
        v
H^s closure / continuation.
```

This is the strongest current P2 architecture because the continuum work is reused only after the finite/native obligations have been discharged.

## 8. Current status

- continuum High–High theorem: **candidate external adapter; independent audit required**;
- finite local absorption inequality checker: **safe exact kernel target**;
- finite-to-dyadic convention map: **OPEN**;
- actual `T_j^{HH}` interval constructor: **OPEN**;
- all-time / all-shell extension and weighted tail summability: **OPEN and Clay-bearing**;
- Clay Navier–Stokes global regularity: **OPEN**.
