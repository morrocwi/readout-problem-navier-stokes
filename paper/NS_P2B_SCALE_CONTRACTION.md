# NS P2B — scale-contraction readout

**Date:** 2026-09-11  
**Parent:** `paper/NS_P2B_FINITE_OBSERVATION_WINDOW_ATTACK.md` / issue #44.  
**Status:** supporting reduction theorem; NSE uniform contraction remains OPEN.  
**Claim boundary:** this is not a Navier--Stokes regularity proof.

## 1. Why introduce a new readout

The finite-observation adapter does not need the full state. It needs its observation term to become small relative to the retained resolution scale. That suggests a dimensionless readout rather than another Sobolev norm.

For `p>2`, define

\[
r_p:=\frac{2p}{p-2}
\]

and, at modal scale `N`,

\[
\boxed{
R_N:=\frac{(K_N^2)^{r_p}}{\Lambda_N}.
}
\]

Up to the fixed viscosity/window/adapter constants, `R_N` is the observation-dependent part of the finite-observation regularity gate divided by its available resolution budget.

The published adapter only needs `R_N` below a fixed positive threshold. Therefore `R_N -> 0` is more than enough.

This is the concrete translation of the Readout Genesis architectural phrase *dynamically closed translation*: instead of asking a large state to remain controlled, ask a finite dimensionless readout to satisfy a closed recursion across resolution.

Genesis supplies the architectural prompt only. The theorem below is elementary mathematics stated and proved here.

## 2. `NS-P2B-SCALE-CONTRACTION`

Take a dyadic sequence of modal scales `N_j` and let `R_j := R_{N_j}`. Suppose finite certificates produce upper bounds

\[
0\le R_j\le U_j
\]

and constants

\[
0\le\kappa<1,\qquad B\ge0,\qquad 0\le\rho<1
\]

such that for every sufficiently large `j`,

\[
\boxed{
U_{j+1}\le \kappa U_j + B\rho^j.
}
\]

Then

\[
U_j\to0,
\qquad
R_j\to0.
\]

Consequently, for any fixed finite positive threshold `R_*`, some finite scale satisfies `R_j<R_*`. Once the exact modal normalization and fixed constants of a validated finite-observation adapter are inserted into `R_*`, that finite scale passes the observation-dependent part of the regularity gate; the other unforced fixed terms are eventually dominated by the resolution side as well.

**Status:** DERIVED reduction conditional on sound certified upper bounds and the displayed all-scale recurrence.

## 3. Proof

Iterating the recurrence from an index `j0` gives

\[
U_j
\le
\kappa^{j-j_0}U_{j_0}
+
B\sum_{m=j_0}^{j-1}\kappa^{j-1-m}\rho^m.
\]

The first term tends to zero because `kappa<1`. The second term is a convolution of two geometric sequences with ratios below one and therefore also tends to zero. Hence `U_j->0`, and `0<=R_j<=U_j` gives `R_j->0`.

No continuum limit object is constructed by this argument; it is a theorem about a finite sequence of certified resolution readouts plus a uniform recurrence law.

## 4. Relationship to the subcritical-exponent theorem

If

\[
K_N^2\le C_T\Lambda_N^{(p-2)/(2p)-\sigma}
\]

with `sigma>0`, then

\[
R_N\le C_T^{r_p}\Lambda_N^{-r_p\sigma}\to0.
\]

Thus `NS-P2B-SUBCRITICAL-OBS` is one sufficient way to generate scale contraction.

The contraction formulation is more flexible: it does not require a pure power law. Logarithmic, piecewise, or certificate-generated improvements can also work if they yield the strict recurrence above.

## 5. Critical-spike falsifier

The P2B energy-budget negative control has, for `p=4`,

\[
(K_N^2)^4=\Lambda_N,
\]

so

\[
R_N=1
\]

at every tested scale.

A constant critical sequence cannot obey a strict contraction with a vanishing defect. Indeed, if `U_j=1` and `kappa<1`, the recurrence requires

\[
\beta_j\ge1-\kappa,
\]

which does not tend to zero.

Therefore the proposed scale-contraction theorem does not accidentally derive regularity from the already-refuted energy-only budget. It demands genuinely new NSE structure.

## 6. Finite certificate language

A finite scale-cell certificate may contain

```text
j
N_j
certified K_N upper bound
certified Lambda_N
U_j >= R_j
kappa
beta_j
```

and verify locally

```text
U_{j+1} <= kappa * U_j + beta_j
0 <= kappa < 1
beta_j <= B * rho^j
0 <= rho < 1
```

using exact rational upper bounds after powers/root enclosures have been certified.

A finite list of such cells is still only a prefix. The Clay-bearing requirement is a **uniform generator/theorem** proving the recurrence for every sufficiently large scale, not a large finite sweep.

## 7. New residual theorem

### `NS-P2B-SCALE-CONTRACTION-UNIFORM` — OPEN / Clay-bearing

Construct from finite/checkable Navier--Stokes structure constants `kappa<1`, `B<infinity`, `rho<1`, an index `j0`, and sound finite observation upper certificates `U_j`, such that

\[
R_{N_j}\le U_j,
\qquad
U_{j+1}\le\kappa U_j+B\rho^j
\]

for every `j>=j0` on every finite target time interval, without assuming regularity.

The natural candidate source of this recursion is the IDM window-transfer balance combined with viscosity, cancellation/flux information, and EPSC-certified finite records. No theorem currently in IDM, Genesis, Universe, or this repository proves the strict `kappa<1` step for actual 3D NSE.

## 8. Ruling

The cross-repository idea therefore advances P2B by replacing the broad phrase *anti-intermittency* with a machine-addressable scale-recursion target:

```text
finite tape / transfer records
 -> certified critical ratios R_j
 -> strict scale contraction
 -> finite observation gate PASS at some finite scale
 -> continuum regularity adapter.
```

`NS-P2B-SCALE-CONTRACTION` is DERIVED.  
`NS-P2B-SCALE-CONTRACTION-UNIFORM` is OPEN/HOLD.  
Clay Navier--Stokes remains OPEN.
