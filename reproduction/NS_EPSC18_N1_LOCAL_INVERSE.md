# EPSC-18 — Full N=1 local inverse witness on a finite symmetry slice

Status: **mixed `finite_diagnostic` + `Dr` + `Open`**.

This note is deliberately finite-first. It does **not** begin from an assumed completed infinite Fourier state. Every object used in the witness is finite: the `N=1` Fourier-Galerkin state has 52 real coordinates, spatial translation contributes three infinitesimal symmetry directions, the shell-energy Taylor jet through order 23 supplies 72 scalar candidate observations, and the certified square minor is `49 x 49`.

## 1. Finite state and translation symmetry

For the cubic cutoff

\[
K_1=\{-1,0,1\}^3\setminus\{0\},
\]

the declared real divergence-free reality-constrained coordinate system has

\[
d_1=52.
\]

Spatial translation acts on a complex Fourier coefficient by

\[
\widehat u_k\mapsto e^{ik\cdot a}\widehat u_k.
\]

If one complex coordinate is written `z=x+iy`, then its infinitesimal translation derivative in direction `a_j` is

\[
\frac{d}{da_j}\bigg|_{a=0}e^{ik\cdot a}z
=i k_jz,
\]

or, in real coordinates,

\[
(x,y)\mapsto(-k_jy,k_jx).
\]

The checker constructs the resulting `52 x 3` translation-tangent matrix `G` at the same exact finite witness used by the existing modular energy-observability calculation.

## 2. Exact modular shell-energy jet

Let `I=(I_1,I_2,I_3)` be the three shell energies for `N=1`. The existing exact modular Taylor construction produces the differential blocks for

\[
I,\ \frac{1}{1!}\frac{dI}{dt},\ldots,
\frac{1}{23!}\frac{d^{23}I}{dt^{23}}
\]

at a fixed integer witness, with viscosity `nu=1/200`, over the good prime

\[
p=1,000,003.
\]

Stacking the 24 three-row blocks gives a `72 x 52` Jacobian `J`. The reproduced rank is

\[
\operatorname{rank}_{\mathbb F_p}J=49.
\]

The checker independently verifies

\[
JG=0\pmod p,
\]

so the known three-dimensional translation tangent lies inside the kernel. Since the nullity is exactly three, at this witness the modular kernel is precisely the translation tangent.

## 3. Explicit finite gauge slice

The checker greedily selects three real coordinate functions whose restriction to the translation tangent has a nonzero `3 x 3` determinant modulo `p`. Fixing those three coordinates gives a 49-dimensional affine coordinate slice transverse to translation at the witness.

Let `J_slice` be the shell-energy Taylor-jet Jacobian restricted to the remaining 49 coordinate directions. Because the slice is transverse to the complete three-dimensional kernel,

\[
\operatorname{rank}_{\mathbb F_p}J_{\rm slice}=49.
\]

The checker then selects 49 observation rows and evaluates the corresponding square determinant directly modulo `p`. A nonzero residue is an explicit finite certificate that this selected minor is not zero in the finite-field reduction.

## 4. Characteristic-zero lift and local inverse

The finite Galerkin map, witness, basis coefficients, viscosity, and Taylor recursion are rational. The only declared denominators in this `N=1`, order-23 construction come from the viscosity denominator, finite polarization-basis norms, and Taylor divisors through 24. The chosen prime does not divide those denominators.

Therefore reduction modulo `p` is valid. If the selected rational determinant were zero in characteristic zero, every good-prime reduction would be zero. Its nonzero residue hence proves

\[
\det D H_{\rm slice}(x_*)\ne0
\]

for the corresponding finite real/rational observation chart `H_slice`.

By the ordinary finite-dimensional inverse-function theorem, there exist neighborhoods `U` of the symmetry-fixed finite state `x_*` and `V` of its observation value such that

\[
H_{\rm slice}:U\to V
\]

has a local real inverse.

This closes a previously missing **local-existence** part of `PROP-EPSC-18` for the complete `N=1` quotient chart.

## 5. What remains open

This result does **not** yet provide the quantity required for a practical measurement certificate,

\[
\inf_{g\in\mathbb T^3}\|P_1u-g\widehat x_1\|\le\rho_1,
\]

with a useful explicit `rho_1` derived from noisy data.

The remaining full `N=1` obligations are quantitative:

1. construct a directed-rounding interval/Krawczyk enclosure on a declared finite box;
2. prove a contraction defect `q<1` there;
3. certify that the true and reconstructed state lie on the same local branch/symmetry slice;
4. propagate measurement-window uncertainty through that inverse.

The existing generic IDM helper states one sufficient condition. If `A` is a fixed preconditioner and a finite interval calculation proves

\[
\sup_{x\in B}\|I-A D H(x)\|\le q<1,
\]

then on the declared branch

\[
\|x-z\|
\le
\frac{\|A\|}{1-q}\|H(x)-H(z)\|.
\]

That is the next target. Rank saturation alone must not be substituted for this radius.

## 6. Relation to finite-first completion

The native result established here is

\[
\text{finite observations}
\longrightarrow
\text{local finite quotient state},
\]

not

\[
\text{finite observations}
\longrightarrow
\text{an assumed infinite state}.
\]

Any later use of a continuum tail `beta_1` is an external analytic adapter. The finite-native inner certificate and the outer adapter remain logically separate.

## Reproduction

Run

```bash
python reproduction/checks/check_volume7_eps18_n1_local_inverse.py
```

or regenerate the complete ledger. The checker reuses the already deposited finite `N=1` Galerkin/Taylor construction in `check_volume6_ns_observability.py` rather than duplicating the PDE algebra.
