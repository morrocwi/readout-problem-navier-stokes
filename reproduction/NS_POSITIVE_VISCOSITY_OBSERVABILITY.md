# Positive-viscosity universality of energy observability

## Status

This note records the strengthened finite result for the first full cubic Fourier--Galerkin truncation

\[
K_1=\{-1,0,1\}^3\setminus\{0\}.
\]

It has 26 nonzero Fourier modes and 52 real divergence-free degrees of freedom. The result is finite-dimensional and does **not** address continuum Navier--Stokes regularity.

## 1. Readers and structural ceilings

Write

\[
\dot x=F_\nu(x)=\nu Ax+B(x,x),\qquad \nu>0,
\]

with the projected quadratic Navier--Stokes interaction `B`. Let `I=(I_1,I_2,I_3)` be the three exact shell energies for `|k|^2 in {1,2,3}` and let

\[
E=\mathbf 1^T I
\]

be total retained kinetic energy. Define the Lie jets

\[
\mathcal J_R=(I,\mathcal L_F I,\ldots,\mathcal L_F^R I),
\]

\[
\mathcal E_R=(E,\mathcal L_F E,\ldots,\mathcal L_F^R E).
\]

The exact shell balance and nonlinear energy conservation imply

\[
\operatorname{rank}D\mathcal J_R\le 3+2R,
\]

while scalar coordinate count gives

\[
\operatorname{rank}D\mathcal E_R\le R+1.
\]

Spatial translations form a 3-dimensional continuous symmetry invisible to both readers, hence

\[
\operatorname{rank}D\mathcal J_R\le 49,
\qquad
\operatorname{rank}D\mathcal E_R\le49.
\]

Therefore

\[
\boxed{\operatorname{rank}D\mathcal J_R\le\min(3+2R,49)},
\]

\[
\boxed{\operatorname{rank}D\mathcal E_R\le\min(R+1,49)}.
\]

Rank 49 is impossible before `R=23` for the shell reader and before `R=48` for the scalar reader.

## 2. Exact finite witness

`checks/check_volume6_ns_observability.py` uses the rational K=1 Galerkin operator, the good prime

\[
p=1{,}000{,}003,
\]

and `nu=1/200`. It propagates formal Taylor and tangent series and computes exact ranks over `F_p`. Because `p>50`, Taylor coefficients and Lie derivatives through order 50 differ only by invertible factorial row scalings.

The checker records

\[
\operatorname{rank}_{\mathbb F_p}D\mathcal J_R=\min(3+2R,49),
\]

\[
\operatorname{rank}_{\mathbb F_p}D\mathcal E_R=\min(R+1,49),
\qquad 0\le R\le50.
\]

A nonzero maximal minor modulo the good prime gives a nonzero characteristic-zero minor polynomial. Together with the structural ceilings this yields generic characteristic-zero rank saturation at `nu=1/200`.

Hence

\[
\boxed{R_{\rm shell}^{\min}=23,\qquad R_{\rm energy}^{\min}=48}.
\]

These are mathematically minimal orders, not merely the first orders observed by the checker.

## 3. Positive-viscosity universality

The fixed-viscosity witness extends to **every** positive viscosity by an exact scaling conjugacy.

Set

\[
x(t)=\nu y(s),\qquad s=\nu t.
\]

Since `B` is quadratic,

\[
F_\nu(\nu y)=\nu^2F_1(y).
\]

Each shell-energy component and total energy is quadratic, so for either reader `h`,

\[
\mathcal L_{F_\nu}^r h(\nu y)
=\nu^{r+2}\mathcal L_{F_1}^r h(y),
\]

and

\[
D_x\mathcal L_{F_\nu}^r h(\nu y)
=\nu^{r+1}D_y\mathcal L_{F_1}^r h(y).
\]

For every `nu>0` these are invertible state and row scalings. Therefore the generic jet ranks are independent of the positive viscosity:

\[
\boxed{
\operatorname{rank}_{\rm gen}D\mathcal J_R=\min(3+2R,49),
\qquad 0\le R\le50,
}
\]

\[
\boxed{
\operatorname{rank}_{\rm gen}D\mathcal E_R=\min(R+1,49),
\qquad 0\le R\le50.
}
\]

In particular,

\[
\boxed{
\operatorname{rank}_{\rm gen}D\mathcal J_{23}=49,
\qquad
\operatorname{rank}_{\rm gen}D\mathcal E_{48}=49,
\qquad \forall\nu>0.
}
\]

The inviscid endpoint is different: at `nu=0`, total kinetic energy is conserved, so the scalar energy jet collapses to `(E,0,0,...)`.

`checks/check_positive_viscosity_scaling.py` reuses the same exact Galerkin operator and checks the vector-field and quadratic-reader scaling identities modulo the project prime for several rational positive viscosities. It is a reproducibility sanity check; the proof is the algebraic identity above.

## 4. Local geometry

At a generic state the translation action is free. It is enough that the coefficients at the three axial modes `e_1,e_2,e_3` are nonzero: any translation fixing such a state must satisfy

\[
e^{ia_1}=e^{ia_2}=e^{ia_3}=1.
\]

Hence the generic stabilizer is trivial and the local quotient by `T^3` is 49-dimensional. At generic regular states,

\[
\boxed{\ker D\mathcal J_{23}(x)=T_x(\mathbb T^3\cdot x)},
\]

\[
\boxed{\ker D\mathcal E_{48}(x)=T_x(\mathbb T^3\cdot x)}.
\]

Thus the only generic **infinitesimally unobservable** directions are spatial translations. Discrete signed coordinate permutations may still create global ambiguities; this is not a global injectivity theorem.

## 5. Resolution-indexed conjecture

For

\[
K_N=\{-N,\ldots,N\}^3\setminus\{0\},
\]

the real zero-mean divergence-free phase-space dimension is

\[
\boxed{d_N=2((2N+1)^3-1)}.
\]

Translation symmetry gives the ceiling `d_N-3`, while a scalar jet cannot attain it before order `d_N-4`.

### Conjecture: energy-readout saturation

For every finite cubic truncation `K_N` and every `nu>0`,

\[
\boxed{
\operatorname{rank}_{\rm gen}D\mathcal E_{d_N-4}=d_N-3.
}
\]

Equivalently, total retained kinetic energy attains the translation-limited generic local observability ceiling at the earliest derivative order allowed by scalar coordinate count.

The present K=1 theorem gives

\[
d_1=52,\qquad R_{\min}=48,\qquad \text{rank}=49.
\]

The next decisive test is `N=2`:

\[
\boxed{d_2=248,\qquad R_{\min}=244,\qquad \text{target rank}=245.}
\]

Failure would expose an additional obstruction; success would establish a second resolution point in the proposed pattern.

## Scope

No claim is made here about continuum regularity, singularity formation, global reconstruction, noisy derivative estimation, or computational speed-up. The finite statement is:

\[
\boxed{
\text{total kinetic energy reaches the exact translation-limited local rank ceiling at the earliest scalar-jet order for K=1 and every }\nu>0.
}
\]
