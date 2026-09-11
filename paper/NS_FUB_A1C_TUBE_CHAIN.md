# NS-FUB-A1C — Finite Validated Tube Chain

**Date:** 2026-09-11  
**Status:** fixed-`N=1` finite-chain candidate until dedicated CI is green.  
**Parent target:** `NS-FUB-A1C-G` remains OPEN as a general/adaptive arbitrary-target generator.

## Purpose

The single-step `NS-FUB-A1C-V` certificate shows that one rational tube can validate a finite Galerkin trajectory over one positive time interval. A constructive witness route needs composition across finitely many intervals without silently replacing an unknown endpoint by an exact state.

This layer therefore carries **interval initial data** from step to step.

## One chain link

Suppose the incoming rational box `I_m` contains the actual finite state at time `t_m`. Choose a larger rational tube box `X_m` and compute exact bounds

\[
|F_i(x)|\le M_{m,i},\qquad x\in X_m,
\]

and

\[
\|DF(x)\|_\infty\le L_m,\qquad x\in X_m.
\]

The link is accepted only if

\[
I_m\subset X_m,
\]

\[
I_m+[0,h_m]F(X_m)\subset X_m,
\]

and

\[
h_mL_m<1.
\]

For every fixed initial point in `I_m`, the Picard map is then a self-map and contraction on paths in `X_m`. The actual endpoint belongs to the rational enclosure

\[
I_{m+1}=I_m+[-h_mM_m,h_mM_m].
\]

Finite induction composes the links.

## Fixed-N calibration generator

`reproduction/checks/check_ns_fub_a1c_n1_tube_chain.py` reuses the exact `N=1` tensor once, starts from the deterministic small-integer point enclosure, and automatically constructs four rational links. At each step it chooses a fresh tube radius larger than the incoming interval halfwidth and a positive rational `h_m` with explicit self-map and contraction slack.

The final interval box is converted into full Fourier coefficient rectangles and passed to `NS-FUB-A1V`.

This is a **finite calibration generator** for a fixed number of steps. It does not establish termination to an arbitrary requested target time.

## Status boundaries

### `NS-FUB-A1C-CV` — finite chain verifier

Given a finite sequence of links satisfying the declared exact inequalities, composition of the trajectory enclosures is `DERIVED` by finite induction plus the per-link contraction theorem.

### `NS-FUB-A1C-G1` — fixed-N finite-step chain constructor

The present executable automatically constructs four links at the pinned `N=1` calibration. Executable PASS status is assigned only after CI succeeds.

### `NS-FUB-A1C-G`

A general/adaptive generator that reaches an arbitrary declared finite target time or returns a mathematically meaningful obstruction, with an appropriate termination/resource theorem and arbitrary admissible finite cutoff: **OPEN**.

### `NS-FUB-A1C-X`

Finite-time singularity forces a constructible validated A1V exceedance certificate: **OPEN**.

## Non-vacuity

Producing more fixed-N links is not by itself progress on the Clay bridge. The value of this chain layer is to remove a logical gap in finite trajectory certification. Clay-level leverage still requires a uniform theorem relating continuation/failure of such finite chains and regularity-sensitive/tail control to the global PDE statement.
