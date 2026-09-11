# NS-FUB-A1 — Stokes tail gain versus recent nonlinear transfer

**Date:** 2026-09-11  
**Tracker:** issue #40.  
**Status:** linear and positive-lag tail estimates DERIVED; recent nonlinear-transfer closure OPEN.  
**Claim boundary:** supporting bridge mathematics only. No Navier--Stokes global-regularity conclusion is promoted.

## 1. Why this split is needed

`NS-FUB-A1-TAIL-L2-NOGO` shows that an instantaneous omitted `L2`/energy tail does not control the omitted `H3` tail. Positive viscosity nevertheless supplies genuine high-frequency damping over any **positive time lag**.

For a periodic mild solution, write

\[
u(t)=e^{\nu\tau\Delta}u(t-\tau)
-\int_{t-\tau}^{t}e^{\nu(t-s)\Delta}\mathbb P\,\operatorname{div}(u\otimes u)(s)\,ds.
\]

More generally, after splitting a Duhamel history at a gap `delta>0`, there are three conceptually different pieces:

```text
linear Stokes memory
+ old nonlinear history with lag >= delta
+ recent nonlinear transfer with lag in (0,delta).
```

The first two admit explicit all-scale high-frequency envelopes. The third is the load-bearing term.

Throughout, `Q_N` denotes the Fourier projection onto modes outside the cube cutoff `[-N,N]^3`. Every retained-outside mode therefore satisfies

\[
q:=|k|^2\ge (N+1)^2.
\]

Use the coefficient-weighted Sobolev norm

\[
\|f\|_{H^3,F}^2=\sum_k(1+|k|^2)^3|\widehat f(k)|^2.
\]

Common torus normalization constants do not affect the estimates.

## 2. Exact rational exponential majorant

For every `x>0` and integer `m>=0`,

\[
e^x=\sum_{j=0}^{\infty}\frac{x^j}{j!}\ge\frac{x^m}{m!},
\]

hence

\[
e^{-x}\le\frac{m!}{x^m}.
\]

This elementary inequality lets the certificate use rational upper envelopes when `nu`, time lags, and cutoffs are rational/integer, without evaluating a floating exponential.

## 3. Linear Stokes tail

### `NS-FUB-A1-STOKES-H3-TAIL`

For `tau>0`,

\[
\|Q_N e^{\nu\tau\Delta}f\|_{H^3,F}^2
\le
\frac{192}{(2\nu\tau)^4(N+1)^2}\,\|f\|_{L^2,F}^2.
\]

### Proof

For one omitted mode with `q=|k|^2>=1`, the squared multiplier is

\[
(1+q)^3e^{-2\nu\tau q}.
\]

Since `(1+q)^3<=8q^3` and, with `x=2 nu tau q` and `m=4`,

\[
e^{-2\nu\tau q}\le\frac{4!}{(2\nu\tau)^4q^4},
\]

we get

\[
(1+q)^3e^{-2\nu\tau q}
\le\frac{8\cdot24}{(2\nu\tau)^4q}
\le\frac{192}{(2\nu\tau)^4(N+1)^2}.
\]

Summing the Fourier coefficients proves the estimate.

For fixed positive `nu,tau`, the certified squared tail multiplier therefore tends to zero at least like `(N+1)^-2`.

## 4. Old nonlinear history with a positive lag

Let `F(s)` be a tensor field and consider

\[
D_{\rm old}(t)=
Q_N\int_0^{t-\delta}
 e^{\nu(t-s)\Delta}\mathbb P\,\operatorname{div}F(s)\,ds,
\qquad \delta>0.
\]

Assume only

\[
A_F:=\int_0^{t-\delta}\|F(s)\|_{L^2,F}\,ds<\infty.
\]

### `NS-FUB-A1-OLD-DUHAMEL-H3-TAIL`

Then

\[
\|D_{\rm old}(t)\|_{H^3,F}^2
\le
\frac{960}{(2\nu\delta)^5(N+1)^2}\,A_F^2.
\]

### Proof

The Leray projector is an orthogonal Fourier multiplier, so its operator norm is at most one. The divergence contributes one factor `|k|`. Thus the squared `L2 tensor -> H3 velocity` multiplier at lag `r=t-s>=delta` is bounded by

\[
(1+q)^3q e^{-2\nu r q}.
\]

For `q>=1`, `(1+q)^3q<=8q^4`. With `m=5`,

\[
e^{-2\nu rq}\le\frac{5!}{(2\nu r)^5q^5}
\le\frac{120}{(2\nu\delta)^5q^5}.
\]

Hence the squared operator multiplier is at most

\[
\frac{960}{(2\nu\delta)^5q}
\le
\frac{960}{(2\nu\delta)^5(N+1)^2}.
\]

Minkowski's integral inequality then gives the displayed bound after integrating `||F(s)||_2` in time.

This is a true positive all-scale tail mechanism for **old history**: any fixed positive lag converts finite `L1_t L2_x` forcing mass into a tail envelope vanishing with `N`.

## 5. Why the recent window is different

For

\[
D_{\rm recent}(t)=Q_N\int_{t-\delta}^{t}
 e^{\nu(t-s)\Delta}\mathbb P\,\operatorname{div}F(s)\,ds,
\]

the lag `r=t-s` approaches zero.

Ignoring the tail cutoff for a moment, the exact Fourier operator multiplier from an `L2` tensor to an `H3` velocity is

\[
m_r(k)=(1+|k|^2)^{3/2}|k|e^{-\nu r|k|^2}.
\]

It has four derivatives of high-frequency demand. The standard heat-semigroup estimate is therefore of order

\[
\|e^{\nu r\Delta}\mathbb P\,\operatorname{div}\|_{L^2\to H^3}
\asymp r^{-2}
\qquad (r\downarrow0).
\]

The lower scaling can be seen directly on torus modes. Let `y=(nu r)^(-1/2)` and, for sufficiently small `r`, choose integer `K=floor(y)>=y/2`. At `k=(K,0,0)`, `nu r K^2<=1`, so `e^{-nu r K^2}>=e^{-1}>1/3`, while

\[
K(1+K^2)^{3/2}\ge K^4.
\]

Consequently

\[
\|e^{\nu r\Delta}\mathbb P\,\operatorname{div}\|_{L^2\to H^3}
\ge\frac{1}{48(\nu r)^2}
\]

for all sufficiently small `r` (using an appropriate tensor polarization for the selected mode).

Thus the operator norm itself is not integrable at the endpoint:

\[
\int_0^{\delta}r^{-2}\,dr=\infty.
\]

### Exact interpretation

This does **not** prove that the Navier--Stokes Duhamel term diverges. The forcing `F=u otimes u` has structure, time dependence, cancellations, and may belong to stronger spaces.

It proves a narrower but important statement:

> the generic `L2`-tensor forcing norm plus the bare heat-semigroup operator estimate cannot by itself close an `H3` bound for the recent nonlinear window.

So the positive Stokes smoothing mechanism stops exactly at the recent nonlinear transfer.

## 6. New finite-bridge target

Define the regularity-sensitive recent-transfer quantity

\[
\mathcal T_{N,\delta}(t):=
\left\|
Q_N\int_{t-\delta}^{t}
 e^{\nu(t-s)\Delta}\mathbb P\,\operatorname{div}(u\otimes u)(s)\,ds
\right\|_{H^3,F}.
\]

A useful next theorem must give a **non-vacuous certified modulus** for this term, or replace it by an equivalent frequency-local flux/cancellation quantity, using information weaker than the desired global `H3` regularity conclusion.

Candidate forms include:

\[
\mathcal T_{N,\delta_N}(t)\le\beta_N,
\qquad \beta_N\to0,
\]

uniformly on the time interval of interest, with a finite/checkable construction of `delta_N,beta_N`; or a shellwise transfer inequality whose summable weighted envelope implies the same conclusion.

The premise must survive the non-vacuity audit: simply assuming a uniform higher-Sobolev norm is mathematically sufficient but does not create new Clay leverage.

## 7. P2 status after the split

- `NS-FUB-A1-STOKES-H3-TAIL`: **DERIVED**.
- `NS-FUB-A1-OLD-DUHAMEL-H3-TAIL`: **DERIVED under the explicit finite forcing-mass assumption**.
- Energy/L2-only instantaneous tail control: **REFUTED** by the prior no-go theorem.
- Fixed-N trajectory/certificate breakdown: **REFUTED as a standalone singularity witness** by the prior fixed-N theorem.
- Recent nonlinear transfer modulus `T_{N,delta}`: **OPEN and load-bearing**.
- General `NS-FUB-A1/A2` and Clay Navier--Stokes regularity: **OPEN**.
