# Positive-viscosity universality of energy observability

## Status

For the finite cubic Fourier--Galerkin truncations

\[
K_N=\{-N,\ldots,N\}^3\setminus\{0\},
\qquad
d_N=2((2N+1)^3-1),
\]

this project now has exact finite scalar-energy observability witnesses at **two** resolutions:

\[
\boxed{
K_1:\ d_1=52,\ \operatorname{rank}_{\rm gen}D\mathcal E_{48}=49,
}
\]

\[
\boxed{
K_2:\ d_2=248,\ \operatorname{rank}_{\rm gen}D\mathcal E_{244}=245.
}
\]

Both orders are the earliest possible for a scalar output, and both statements hold for every positive viscosity. These are finite-Galerkin results, not continuum regularity claims.

## 1. Structural ceiling and optimal scalar order

Write

\[
\dot x=F_\nu(x)=\nu Ax+B(x,x),\qquad \nu>0,
\]

and let total retained kinetic energy be

\[
E(x)=\frac12\sum_{k\in K_N}|\widehat u_k|^2.
\]

Define

\[
\mathcal E_R=(E,\mathcal L_F E,\ldots,\mathcal L_F^R E).
\]

Spatial translations form a 3-dimensional continuous symmetry invisible to `E`, so at generic states

\[
\operatorname{rank}D\mathcal E_R\le d_N-3.
\]

A scalar jet has only `R+1` coordinates, hence

\[
\boxed{
\operatorname{rank}D\mathcal E_R\le\min(R+1,d_N-3).
}
\]

Therefore the symmetry ceiling cannot be reached before

\[
\boxed{R=d_N-4.}
\]

## 2. Exact finite witnesses

### K=1

`checks/check_volume6_ns_observability.py` gives an exact modular witness for the 52-dimensional cube. The scalar energy rank reaches

\[
49=d_1-3
\]

first at

\[
48=d_1-4.
\]

### K=2

`checks/check_k2_energy_observability.py` uses the 124 retained nonzero Fourier modes of `K_2`, giving

\[
d_2=248.
\]

It propagates the formal Taylor state and 245 projected tangent directions exactly over the good prime

\[
p=251
\]

at `nu=1/200`. Because `251>244` and all declared Galerkin/basis/viscosity denominators are invertible, Taylor-output and Lie-derivative ranks agree through order 244 up to invertible factorial row scalings.

The recorded scalar ranks include

\[
\begin{array}{c|cccccccc}
R&10&30&60&120&180&220&243&244\\\hline
\operatorname{rank}&11&31&61&121&181&221&244&245.
\end{array}
\]

Thus the projected `245 x 245` Jacobian is nonsingular at `R=244`. The full energy-jet Jacobian therefore has row rank 245 over `F_251`; a corresponding characteristic-zero maximal minor is not identically zero. Combining this with the translation ceiling gives

\[
\boxed{
\operatorname{rank}_{\rm gen}D\mathcal E_{244}=245.
}
\]

Since all smaller `R` satisfy `R+1<245`, the order 244 is optimal.

The machine-readable output is `results/k2_energy_observability_mod251.json`, and the focused derivation is `NS_K2_ENERGY_OBSERVABILITY.md`.

## 3. Positive-viscosity universality

The exact scaling

\[
x(t)=\nu y(\nu t),
\qquad
F_\nu(\nu y)=\nu^2F_1(y)
\]

uses only the linear viscous term and quadratic homogeneity of `B`. Since energy is quadratic,

\[
\mathcal L_{F_\nu}^rE(\nu y)
=\nu^{r+2}\mathcal L_{F_1}^rE(y),
\]

\[
D_x\mathcal L_{F_\nu}^rE(\nu y)
=\nu^{r+1}D_y\mathcal L_{F_1}^rE(y).
\]

For every `nu>0` these are invertible state and row scalings. Therefore the generic rank is independent of positive viscosity. In particular,

\[
\boxed{
K_1:\ \operatorname{rank}_{\rm gen}D\mathcal E_{48}=49,
\qquad
K_2:\ \operatorname{rank}_{\rm gen}D\mathcal E_{244}=245,
\quad\forall\nu>0.
}
\]

The endpoint `nu=0` is different because total kinetic energy is conserved.

## 4. Local geometry

At generic states the translation action is free; the axial modes force any stabilizing translation to be trivial. Consequently the local quotient has dimension `d_N-3`. At the two proved saturation points,

\[
\ker D\mathcal E_{d_N-4}(x)
=
T_x(\mathbb T^3\cdot x),
\qquad N=1,2,
\]

generically. Thus the only generic infinitesimally unobservable directions are spatial translations. Discrete lattice symmetries may still cause global ambiguities, so this is not global injectivity.

## 5. Resolution-indexed conjecture

The first two cubic resolutions now support the same exact pattern:

\[
\boxed{
N=1:\ 52\to49\text{ at }R=48,
\qquad
N=2:\ 248\to245\text{ at }R=244.
}
\]

This motivates the still-open general conjecture:

\[
\boxed{
\operatorname{rank}_{\rm gen}D\mathcal E_{d_N-4}=d_N-3
\qquad
\text{for every finite }K_N\text{ and every }\nu>0.
}
\]

No claim is made here about continuum Navier--Stokes regularity, singularity formation, stable recovery from noisy high-order derivatives, global reconstruction, or computational speed-up.
