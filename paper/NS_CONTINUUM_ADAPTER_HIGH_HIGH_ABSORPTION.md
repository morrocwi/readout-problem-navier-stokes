# NS P2 — High–High absorption as a continuum semantic-adapter candidate

**Date:** 2026-09-11  
**Tracker:** issue #41.  
**Status:** candidate adapter **HOLD after independent audit**.  
**Claim boundary:** no global-regularity claim. The external source is a non-peer-reviewed preprint; its current theorem/proof package is not accepted as a validated final adapter.

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
  independently proved regularity implication
          |
          v
GLOBAL REGULARITY CONSEQUENCE
```

The Clay-strength work is on the first arrow. A continuum theorem may close the second arrow only if its hypotheses have already been established without circularly assuming the desired regularity **and** the continuum theorem itself survives independent audit.

## 2. External High--High candidate

A structurally aligned candidate is:

Shin-ichi Inage, *Conditional Regularity of the Three-Dimensional Navier–Stokes Equations via High–High Triadic Absorption*, Preprints.org, version 1 posted 20 March 2026, DOI `10.20944/preprints202603.1591.v1`.

The source presents its main regularity theorem as conditional, not as an unconditional solution of the 3D Navier--Stokes global-regularity problem. The posted version is a preprint and is not peer-reviewed.

Its intended continuum condition is schematically

\[
T_j^{HH}(t)\le \eta V_j(t)+\rho_j(t),
\]

plus Sobolev-weighted control of `rho_j`, followed by a weighted energy estimate and continuation for `s>5/2`.

This architecture is useful as a **translation target**. The current preprint, however, is not accepted as the final semantic adapter for the reasons below.

## 3. Independent audit findings — adapter HOLD

### A. Absorption-parameter mismatch

The theorem statement permits `eta in (0,1)`, but the displayed proof later requires

\[
0<\eta<\frac34 c_0
\]

in order to leave a positive viscous coefficient after the Low--Low/Low--High allocation and High--High absorption. Under the paper's displayed dyadic normalization one has `D_j >= V_j`, so a safe direct mapping uses `c_0=1` and therefore

\[
\boxed{0\le\eta<3/4}
\]

rather than merely `eta<1`.

Our finite checker consequently treats `3/4` as the conservative cap when testing this particular candidate adapter. A different independently proved adapter may use a different certified cap.

### B. Main-text linear closure is not supplied by the appendix estimate

The main argument requires a linear weighted estimate of the form

\[
\frac{d}{dt}X_s + c_1Y_s\le C(1+X_s)
\]

so that Gronwall closes the `H^s` norm.

But the appendix's displayed Low--High summation gives a term of order

\[
\|u\|_{H^s}^3 = X_s^{3/2},
\]

and then records an inequality containing that cubic term before subsequently writing the desired linear inequality without a displayed derivation that removes or absorbs the cubic contribution. The missing step is load-bearing: `X_s^{3/2}` cannot simply be replaced by `C(1+X_s)` with a solution-independent constant.

Therefore the current text does not establish the claimed linear Gronwall closure from the displayed appendix bounds.

### C. Weighted remainder model does not by itself justify the infinite-shell sum

The appendix models a remainder with scale comparable to

\[
\rho_j\lesssim 2^{-2sj}\|u\|_{H^s}^2.
\]

Multiplying by the theorem's Sobolev weight `2^{2sj}` leaves a quantity of constant order in `j`. Such a model does not yield an infinite weighted sum unless an additional decaying factor, finite support theorem, or other summability mechanism is proved. A statement that only finitely many shells contribute is not available for a general smooth continuum solution.

This is exactly the all-shell gap that the finite-first programme refuses to hide.

### Audit ruling

```text
Inage High--High preprint as final continuum adapter: HOLD
```

The shellwise absorption idea remains useful as a candidate *subroute*, but no P2 or Clay conclusion may depend on the current preprint as if its continuum closure were already established.

## 4. Finite certificate language retained as a reusable interface

For a finite shell/time cell `(j,I)`, define

\[
\mathcal A_{j,I}=
(j,I,\eta,T^+_{j,I},V^-_{j,I},\rho^+_{j,I},w_j),
\]

where all numeric fields are rational and

- `T^+` is a certified upper bound on a declared nonlinear shell-transfer quantity;
- `V^-` is a certified lower bound on the matching viscous shell quantity;
- `rho^+ >= 0` is the declared remainder budget;
- `eta` is a rational absorption parameter;
- `w_j` is the declared Sobolev shell weight.

The local verifier accepts only if

\[
T^+_{j,I}\le \eta V^-_{j,I}+\rho^+_{j,I}.
\]

For the audited Inage mapping it additionally requires

\[
0\le\eta<3/4.
\]

The checker is fail-closed and does not infer the truth of the continuum theorem.

## 5. Finite weighted remainder verifier

For a finite shell range `j0 <= j <= J`, exact rational arithmetic can verify

\[
R_{\le J}:=\sum_{j=j_0}^{J} w_j\rho^+_j.
\]

A finite prefix is never silently promoted to an infinite sum. The separate theorem `NS-P2-HH-GEOM-LIFT` in `paper/NS_P2_FINITE_TO_CONTINUUM_CLOSURE.md` gives one exact sufficient translation when the true tail defect has a certified geometric envelope with `64q<1` in the `H^3` case.

## 6. Translation obligations if a corrected High--High adapter is pursued

A corrected/self-contained High--High route would still need:

1. a convention map from repository Fourier/Galerkin shells to the continuum dyadic decomposition;
2. sound finite enclosures of the chosen nonlinear transfer and viscous quantity;
3. time-cell coverage;
4. an all-shell tail theorem;
5. weighted remainder summability;
6. a separately proved continuum energy closure, including every Low--Low/Low--High term with constants that genuinely give a linear/subcritical differential inequality.

Until item 6 is proved, High--High absorption is not the main P2 adapter.

## 7. Main P2 route after the audit

The main route is now adapter-neutral. Define the full finite-Galerkin `H^3` nonlinear production and viscous dissipation

\[
\mathcal P_N(t)
:=\left\langle \Lambda^3u_N,
\Lambda^3\bigl[-P_N(u_N\cdot\nabla u_N)\bigr]\right\rangle,
\]

\[
\mathcal D_N(t)
:=\nu\|\nabla\Lambda^3u_N\|_2^2,
\qquad
X_N(t):=\|u_N(t)\|_{H^3}^2.
\]

The clean residual target is a uniform finite certificate theorem producing constants `theta<1` and `C_T<infinity`, independent of `N`, such that

\[
\boxed{
\mathcal P_N(t)
\le \theta\mathcal D_N(t)+C_T(1+X_N(t))
}
\]

for every cutoff and every time in the target finite interval.

This directly yields a uniform `H^3` differential inequality and therefore needs only the standard Galerkin/continuation semantic adapter at the end. The High--High geometric route is one possible method for proving this margin, not an assumed continuum theorem.

## 8. Current status

- finite local absorption checker: **PASS as an exact arithmetic interface**;
- `NS-P2-HH-GEOM-LIFT`: **DERIVED** as an adapter-neutral weighted-tail lifting lemma;
- Inage preprint as final continuum adapter: **HOLD**;
- corrected/self-contained High--High continuum closure: **OPEN**;
- full uniform `H^3` dissipative-margin theorem: **OPEN and load-bearing**;
- Clay Navier--Stokes global regularity: **OPEN**.
