# Residual-Based Relative-Energy Adapter from a Finite Fourier Path to Leray--Hopf Navier--Stokes

**Status:** analytic derivation (`Dr`) plus an exact finite continuous-time tape enclosure (`finite_diagnostic`).  
**Date:** 2026-09-10.  
**Scope:** periodic incompressible Navier--Stokes; comparison with a finite Fourier path having the regularity required by the relative-energy argument.  
**Non-claim:** no global regularity, singularity, uniqueness-for-all-weak-solutions, DNS-adequacy, or Clay Millennium claim.

This note addresses `PROP-EPSC-12`: how can a finite Fourier computation be connected to an **actual** Leray--Hopf continuum solution strongly enough to drive a terminal epsilon certificate?

The key is not to assume that a Galerkin trajectory equals `P_Ku`. Instead, treat a finite path as an approximate solution, compute its full equation residual, and use the standard relative-energy inequality to bound its distance from a Leray--Hopf solution with the same declared data. `PROP-EPSC-15` now supplies the continuous-time finite path and certified residual summaries directly from a stored binary64 RK4 node tape.

---

## 1. Approximate finite path and residual

Let `u` be a Leray--Hopf weak solution of

\[
\partial_tu+P[(u\cdot\nabla)u]-\nu\Delta u=Pf,
\qquad \nabla\cdot u=0,
\]

on the periodic three-torus.

Let `v` be a divergence-free comparison path with sufficient regularity and define

\[
\boxed{
r
:=
\partial_tv+P[(v\cdot\nabla)v]-\nu\Delta v-Pf.
}
\]

Thus `v` obeys the target equation exactly when `r=0`.

For an exact `K`-Galerkin semidiscrete path with unforced dynamics, the in-cube residual is zero by construction and the unresolved residual is

\[
r_K=(I-P_K)P[(v_K\cdot\nabla)v_K].
\]

Because `v_K` is supported in the `K` cube, this quadratic residual is supported in the finite `2K` cube.

---

## 2. Relative-energy adapter theorem

Write

\[
w=u-v,
\qquad y(t)=\|w(t)\|_2^2.
\]

Subtract the equations and test by `w`. Periodicity and incompressibility give the standard relative-energy inequality

\[
\frac12y(t)+\nu\int_0^t\|\nabla w\|_2^2ds
\le
\frac12y(0)
+
\int_0^t\|\nabla v\|_\infty y(s)ds
+
\int_0^t|\langle r,w\rangle|ds.
\]

Using

\[
|\langle r,w\rangle|
\le
\|r\|_{H^{-1}}\|\nabla w\|_2
\le
\frac{1}{2\nu}\|r\|_{H^{-1}}^2
+
\frac\nu2\|\nabla w\|_2^2,
\]

we obtain

\[
y(t)
\le y(0)
+2\int_0^t\|\nabla v\|_\infty y(s)ds
+\frac1\nu\int_0^t\|r\|_{H^{-1}}^2ds.
\]

Define

\[
A_T:=2\int_0^T\|\nabla v(t)\|_\infty dt,
\qquad
B_T:=\int_0^T\|r(t)\|_{H^{-1}}^2dt,
\]

and let `e_0` be any certified upper bound on `||u_0-v(0)||_2`.

### Theorem 1 -- residual-based terminal adapter

\[
\boxed{
\sup_{0\le t\le T}\|u(t)-v(t)\|_2^2
\le
\exp(A_T)\left(e_0^2+\frac{B_T}{\nu}\right).
}
\]

### Proof

Apply Gronwall to the preceding scalar inequality. This is a standard weak--strong/relative-energy stability argument; no originality is claimed for that analytic ingredient.

---

## 3. Direct terminal Fourier-tail certificate

If

\[
v(T)=P_Kv(T),
\]

then

\[
(I-P_K)u(T)=(I-P_K)(u(T)-v(T)),
\]

so

\[
\boxed{
\|(I-P_K)u(T)\|_2
\le
\beta_K^{RE}(T)
:=
\exp(A_T/2)
\left(e_0^2+\frac{B_T}{\nu}\right)^{1/2}.
}
\]

A finite trajectory with a certified full residual can therefore yield a prescribed terminal `L2` Fourier-tail certificate without asserting that the trajectory equals the continuum projection.

The certificate may be loose because of the gradient majorant and exponential. Looseness affects usefulness, not the direction of the bound.

---

## 4. Integrated gradient-error bound

Let

\[
E_T^2
:=
\exp(A_T)\left(e_0^2+\frac{B_T}{\nu}\right).
\]

The absorbed relative-energy inequality yields

\[
\boxed{
\int_0^T\|\nabla(u-v)\|_2^2dt
\le
\frac1\nu
\left(
e_0^2+A_TE_T^2+\frac{B_T}{\nu}
\right).
}
\]

Thus, with

\[
Z_T
:=
\left[
\frac1\nu
\left(e_0^2+A_TE_T^2+\frac{B_T}{\nu}\right)
\right]^{1/2},
\]

for a `K`-supported comparison path,

\[
\|P_Ku(T)\|_2
\ge
\max\{0,\|v(T)\|_2-E_T\},
\]

and

\[
\|\nabla P_Ku\|_{L^2_tL^2_x}
\ge
\max\{0,\|\nabla v\|_{L^2_tL^2_x}-Z_T\}.
\]

This connects the relative-energy route with the separate terminal energy-budget certificate.

---

## 5. Finite Fourier residual algebra

For

\[
v(x,t)=\sum_{k\in\mathcal K_K}\widehat v_k(t)e^{ik\cdot x},
\]

a conservative coefficient bound is

\[
\|\nabla v(t)\|_\infty
\le
\sum_{k,i,j}|k_j|\,|\widehat v_{k,i}(t)|.
\]

For a `K`-supported state, every quadratic output lies in the finite `2K` cube. With the normalized `2\pi`-periodic convention,

\[
\boxed{
\|r(t)\|_{H^{-1}}^2
=
\sum_{q\ne0}
\frac{|\widehat r_q(t)|^2}{|q|_2^2}.
}
\]

So once a continuous finite Fourier path is declared, both adapter integrands are finite algebraic objects.

---

## 6. PROP-EPSC-15: exact path from the stored binary64 RK4 tape

The previous version of this note left one numerical obligation open: node values alone do not certify time integrals. That obligation is now met by a different choice of comparison path.

Let the stored RK4 node values be binary64 numbers. For each real and imaginary component, use its **exact IEEE-754 dyadic rational value**. Apply the Fourier Leray projector in exact rational arithmetic, obtaining divergence-free node records `v_n`. Define, on each cell of width `h`,

\[
\boxed{
v_h(t_n+\theta h)
=(1-\theta)v_n+\theta v_{n+1},
\qquad 0\le\theta\le1.
}
\]

The path is continuous and piecewise smooth, is exactly `K`-supported, and is exactly divergence-free. It is **not** asserted to solve the Galerkin ODE. Instead, its defect against the full PDE is computed.

### 6.1 Exact residual polynomial

On a cell each Fourier coefficient has the form

\[
\widehat v_k(\theta)=a_k+\theta d_k.
\]

Hence

\[
\partial_t\widehat v_k=d_k/h
\]

is constant, viscosity is affine in `theta`, and the quadratic convection term has degree at most two. Therefore

\[
\widehat r_q(\theta)=c_{q,0}+c_{q,1}\theta+c_{q,2}\theta^2.
\]

Consequently

\[
\|r_h(\theta)\|_{H^{-1}}^2
=
\sum_{q\ne0}\frac{|c_{q,0}+c_{q,1}\theta+c_{q,2}\theta^2|^2}{|q|^2}
\]

is a nonnegative polynomial of degree at most four. Its cell integral is a finite rational sum using

\[
\int_0^1\theta^{m+n}\,d\theta=\frac1{m+n+1}.
\]

Thus `B_T` for this declared path is evaluated exactly after tape capture.

### 6.2 Rigorous gradient integral majorant

For each complex coefficient,

\[
|z|\le |\Re z|+|\Im z|.
\]

Because real and imaginary parts are affine in `theta`, convexity gives

\[
\int_0^1 |(1-\theta)a+\theta b|\,d\theta
\le \frac{|a|+|b|}{2}.
\]

Applying this coefficientwise yields a rational upper bound `G_bar` for

\[
\int_0^T\|\nabla v_h\|_\infty dt,
\]

and `A_bar=2 G_bar`.

### 6.3 Rigorous exponential and square root

The executable checker upper-bounds `exp(A_bar)` by a rational Taylor partial sum plus a geometric majorant for the positive remainder. The reported decimal `beta` is rounded upward using integer square-root arithmetic. Therefore the final finite summary never relies on a downward-rounded transcendental evaluation.

### 6.4 What the construction buys

The end-to-end chain is now

```text
stored binary64 RK4 node tape
  -> exact dyadic capture
  -> exact rational Leray projection
  -> continuous piecewise-linear finite Fourier path
  -> exact/rigorous A_bar and B_bar
  -> PROP-EPSC-13 relative-energy theorem (Dr)
  -> terminal continuum L2 / omitted-tail beta
```

Time-discretization error and interpolation error are not separately guessed: they are part of the full PDE residual and therefore enter `B_bar` automatically.

---

## 7. Executed witness

`reproduction/checks/check_volume7_rk4_continuous_enclosure.py` executes the construction on two cases.

For a short Taylor--Green `K=1` tape with `nu=0.01`, `dt=0.01`, `T=0.05`, the recorded finite run gives approximately

\[
\overline A_T=0.599550229412277,
\qquad
\overline B_T=9.736386925864618\times10^{-5},
\]

and

\[
\beta_T\le0.1331648457569634.
\]

All certification arithmetic after binary64 tape capture is exact rational arithmetic. The same checker runs a shear-decay sanity case and verifies that the resulting certified radius dominates the known analytic terminal error.

These numbers demonstrate the certificate construction on a small run. They do **not** establish turbulence/DNS adequacy of `K=1`, nor do they assert that the bound is tight.

---

## 8. Four-repository consequence

### Information Discrete Mathematics

Reusable implementation:

- `idm/ns_relative_energy_adapter.py` -- analytic adapter algebra and snapshot helpers;
- `idm/ns_rk4_path_certificate.py` -- exact-dyadic piecewise-linear continuous-time `A/B` enclosure.

### Toledo

`PROP-EPSC-15` records the exact piecewise-linear tape enclosure. `PROP-EPSC-16` separates the next problem -- high-cutoff tightness and computational scaling -- from correctness of the finite construction.

### Readout Genesis

The application instantiates the rule that a sufficient retained record may be a **trajectory certificate**, not merely a terminal state. The retained object relevant to the continuum adapter is

\[
\mathcal R_K^{RE}=(e_0,\overline A_T,\overline B_T).
\]

### Readout-Navier-Stokes

This repository owns the NS specialization, executable witness, generated ledger and manuscript.

---

## 9. Claim boundary

Derived at standard analytic (`Dr`) tier:

- the residual-based relative-energy error bound;
- the direct terminal omitted-tail corollary for `K`-supported comparison paths;
- the integrated gradient-error bound;
- the directional retained-energy-tape bounds.

Executed at `finite_diagnostic` tier:

- exact dyadic capture of recorded binary64 node values;
- exact rational Leray projection;
- exact polynomial residual integration for the piecewise-linear finite Fourier path;
- rigorous coefficientwise gradient-integral majorant;
- rational upper enclosure of the exponential and upward-rounded terminal radius;
- Taylor--Green and analytic-shear finite witnesses.

Still open:

- tight and affordable certification at substantially larger `K` and longer `T` (`PROP-EPSC-16`);
- unconditional pointwise global regularity in 3-D;
- physical/DNS adequacy of coarse cutoffs;
- finite-time singularity versus global smoothness;
- the Clay Millennium problem.

The previous “finite solver -> ??? -> continuum” gap is therefore narrowed to a declared and executable finite path certificate followed by a standard analytic relative-energy implication. The correctness construction and the high-resolution usefulness problem are now kept separate.
