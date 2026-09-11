# NS-FUB-A1 — Energy-only tail suppression no-go

**Date:** 2026-09-11  
**Status:** analytic finite/Fourier counterexample theorem; exact regression checker accompanies this note.  
**Tracker:** issue #34.  
**Claim boundary:** this refutes an insufficient tail premise. It does not prove or disprove Navier--Stokes global regularity.

## 1. Question

A remaining `NS-FUB-A1` candidate is a finite scale-extension/tail certificate. The weakest tempting form is:

> if the omitted Fourier tail has small energy/L2 norm, then its regularity-sensitive H3 contribution is controlled.

That implication is false, even for one real divergence-free Fourier mode pair.

Throughout this note use the standard coefficient-weighted Sobolev quantities (up to the common torus normalization constant)

\[
\|u\|_{L^2,F}^2=\sum_k |\hat u_k|^2,
\qquad
\|u\|_{H^3,F}^2=\sum_k(1+|k|^2)^3|\hat u_k|^2.
\]

Only the ratio of the frequency weights matters below.

## 2. No-go theorem

### `NS-FUB-A1-TAIL-L2-NOGO`

For every finite cutoff `N`, every `epsilon>0`, and every finite target `B>0`, there exists a real divergence-free Fourier field supported entirely above `N` such that

\[
\|u_{>N}\|_{L^2,F}\le\epsilon
\]

but

\[
\|u_{>N}\|_{H^3,F}>B.
\]

### Construction

Choose an integer `K>N`, let

\[
k=(K,0,0),\qquad e=(0,1,0),
\]

and set the only nonzero Fourier coefficients to

\[
\hat u_k=a e,\qquad \hat u_{-k}=a e,
\qquad a=\epsilon/2.
\]

The conjugate pair gives a real field. Since `k dot e=0`, it is divergence-free.

Its squared L2 tail is

\[
2a^2=\epsilon^2/2\le\epsilon^2,
\]

whereas its squared H3 tail is

\[
2(1+K^2)^3a^2
=\frac{\epsilon^2}{2}(1+K^2)^3.
\]

The latter tends to infinity as `K -> infinity`, so `K` can be chosen with `K>N` and

\[
\frac{\epsilon^2}{2}(1+K^2)^3>B^2.
\]

This proves the claim.

## 3. Strong consequence

For fixed `N` and fixed positive `epsilon`,

\[
\sup\left\{
\|v\|_{H^3,F}:
\operatorname{supp}\hat v\subset\{|k|>N\},
\ \|v\|_{L^2,F}\le\epsilon,
\ \nabla\cdot v=0
\right\}=\infty.
\]

Therefore there is no finite function of only `(N, epsilon)` that bounds the H3 tail of all divergence-free fields with L2 tail at most `epsilon`.

In particular, an energy inequality or an L2 omitted-tail estimate by itself cannot supply the regularity-sensitive all-scale tail budget required by `NS-FUB-A1/A2`.

## 4. Finite-band variant and why it does not solve the problem

If the omitted part is known to live only in a finite band `N<|k|<=M`, then trivially

\[
\|u_{N<\cdot\le M}\|_{H^3,F}^2
\le (1+M^2)^3\|u_{N<\cdot\le M}\|_{L^2,F}^2.
\]

But this constant diverges as `M -> infinity`. It is therefore a finite-band estimate, not an all-scale bridge.

## 5. A mathematically sufficient repair template

If one independently has a stronger weighted tail budget, for example for some `sigma>0`

\[
\|u_{>N}\|_{H^{3+\sigma},F}^2\le C,
\]

then

\[
\|u_{>N}\|_{H^3,F}^2
\le (1+N^2)^{-\sigma} C.
\]

This follows termwise because for `|k|>N`,

\[
(1+|k|^2)^3
\le (1+N^2)^{-\sigma}(1+|k|^2)^{3+\sigma}.
\]

This is only a **repair template**, not a Clay route: a uniform `H^{3+sigma}` bound may be stronger than the desired regularity control and therefore fails the non-vacuity test unless a genuinely finite/PDE mechanism proves it without already assuming global smoothness.

## 6. P2 ruling

The candidate witness class `finite scale-extension/tail suppression` is narrowed as follows.

- **REFUTED:** energy/L2 tail smallness alone -> uniform H3 tail control.
- **INSUFFICIENT:** finite-band energy bounds whose constant grows like `(1+M^2)^3` with the outer cutoff.
- **OPEN:** a PDE-derived, frequency-weighted, all-scale/summable tail mechanism that is regularity-sensitive and non-vacuous.

This means the next positive bridge must carry genuine high-frequency information; total energy alone cannot do the job.
