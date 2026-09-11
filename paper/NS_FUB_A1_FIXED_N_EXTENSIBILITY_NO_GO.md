# NS-FUB-A1 — Fixed-N extensibility failure is not a singularity witness

**Date:** 2026-09-11  
**Tracker:** issue #38.  
**Status:** analytic fixed-dimensional Galerkin theorem plus exact N=1 implementation calibration.  
**Claim boundary:** this removes an invalid fixed-cutoff failure class. It does not prove continuum regularity.

## 1. Candidate being audited

One proposed `NS-FUB-A1` failure class was:

```text
finite certificate recursion/extensibility fails
    -> possible finite singularity witness.
```

At a **fixed** Fourier-Galerkin cutoff this is not an intrinsic dynamical obstruction. The finite Galerkin system has a global trajectory for every finite time, and in the fixed rational finite-data setting the residual-certificate language is complete enough to enclose that trajectory on finite horizons.

## 2. Fixed-N Galerkin global extension

Let `V_N` be any finite-dimensional divergence-free Fourier-Galerkin space and let `P_N` be the orthogonal projection onto it. The unforced periodic Galerkin system is

\[
\partial_t u_N + \nu A u_N + P_N B(u_N,u_N)=0,
\qquad \nu>0,
\]

with `A=-Delta` and `B(u,u)=P(u dot grad u)` in the divergence-free formulation.

Taking the `L2` inner product with `u_N`, orthogonality of `P_N` and the standard incompressible cancellation give

\[
\langle P_N B(u_N,u_N),u_N\rangle
=\langle B(u_N,u_N),u_N\rangle=0.
\]

Hence

\[
\frac12\frac{d}{dt}\|u_N\|_2^2
+\nu\|\nabla u_N\|_2^2=0.
\]

Therefore

\[
\|u_N(t)\|_2\le\|u_N(0)\|_2
\]

for every time in the maximal ODE interval.

The Galerkin right-hand side is a polynomial map on a finite-dimensional vector space, hence locally Lipschitz. A finite-dimensional ODE can fail to extend at a finite maximal time only if the state leaves every bounded set. The energy identity prevents that. Thus:

### `NS-FUB-A1-FIXEDN-GLOBAL`

For every fixed finite cutoff `N`, positive viscosity, and finite initial Galerkin state, the Fourier-Galerkin trajectory exists for all finite times.

**Status:** DERIVED by the finite-dimensional energy argument above.

## 3. Certificate consequence in the rational finite-data setting

The previously merged result `NS-FUB-A1C-COMP-Q` establishes completeness of the residual-centered rational certificate language for strict finite witnesses at a fixed rational polynomial/Galerkin ODE. Its proof mechanism first constructs finite rational residual trajectory tubes; the strict observable margin is only needed for the final observable decision.

The same compact-trajectory/rational-approximation argument therefore gives the trajectory-only corollary:

### `NS-FUB-A1C-CHAIN-EXIST-Q`

For a fixed finite rational Galerkin ODE, rational initial state, and rational finite target time `T`, there exists a finite rational residual-centered validated tube chain enclosing the exact finite Galerkin trajectory on `[0,T]`.

No polynomial runtime or practical search bound is claimed.

## 4. No-go consequence

Combining fixed-N global existence with fixed-finite certificate completeness gives:

### `NS-FUB-A1-CERTFAIL-NOGO`

In the fixed rational finite-data setting, the statement

```text
there exists no valid finite trajectory certificate to time T
```

cannot be a genuine dynamical failure of the Galerkin Navier--Stokes system.

If a particular integrator, interval scheme, search budget, or certificate constructor returns HOLD/FAIL at fixed `N`, that may reflect:

- a weak enclosure language;
- wrapping/conditioning;
- resource limits;
- a poor reference path or step strategy;
- search incompleteness;

but not nonexistence of the finite Galerkin trajectory.

Therefore **fixed-N certificate failure alone is REFUTED as a continuum singularity witness**.

## 5. What may still carry Clay leverage

Only a statement with a proved all-scale connection can remain relevant, for example a quantitative deterioration such as

\[
\Gamma_N(T)\to\infty
\]

or loss of a positive margin as `N -> infinity`, where `Gamma_N` is explicitly tied by theorem to a regularity-sensitive norm, a tail envelope, or a compactness/continuation criterion.

Merely observing that certificate size, interval width, conditioning, or runtime worsens with `N` is not enough. The deterioration must have a proved PDE meaning.

The viable candidate is thus narrowed from

```text
fixed-N certificate recursion failure
```

to

```text
uniform-in-N loss of a PDE-relevant certified modulus / margin
    + explicit theorem connecting that loss to regularity.
```

## 6. Exact N=1 implementation cross-check

`reproduction/checks/check_ns_fub_a1_fixed_n_energy_extensibility.py` reconstructs the existing exact integer-scaled N=1 Galerkin quadratic tensor and its physical coordinate energy weights. It aggregates every cubic coefficient of

\[
\sum_i w_i x_i (C B(x,x))_i
\]

and requires the resulting polynomial to vanish identically coefficient-by-coefficient. It also verifies that the scaled viscous diagonal is strictly negative on every nonzero retained mode.

This is an implementation calibration of the analytic energy cancellation, not a machine proof of the all-N theorem.

## 7. Remaining P2 frontier

After this no-go, the useful failure classes are genuinely **uniform** ones:

1. regularity-sensitive finite norm exceedance (`A1E/A1V`);
2. loss of a frequency-weighted, summable/all-refinement tail envelope;
3. uniform-in-N deterioration only when a separate PDE theorem makes that deterioration regularity-relevant.

General `NS-FUB-A1`, `NS-FUB-A2`, and Clay Navier--Stokes regularity remain OPEN.
