# Energy-transfer observability bridge

Status: `Dr` + `finite_diagnostic` + `Open`, with explicit boundaries below.

This note connects the finite energy-observability lane to EPSC without importing the Readout Genesis interpretation as a physical theorem. Genesis motivates the language of **restoration** and **transmitted difference**; the actual Navier-Stokes claims below are owned by finite Fourier-Galerkin algebra and standard energy identities.

## 1. Shell balance separates redistribution from dissipation

For a shell label `s=|k|^2`, define the retained shell kinetic energy `I_s` in the same normalization as the observability paper. For the unforced finite Fourier-Galerkin Navier-Stokes system,

\[
\dot I_s=T_s-2\nu s I_s,
\]

and, because the quadratic incompressible nonlinearity conserves total kinetic energy inside the finite closed truncation,

\[
\sum_sT_s=0.
\]

With a prescribed shell-energy input `F_s`, add `+F_s` to the balance. This decomposition is standard NS bookkeeping; no originality claim is made for it.

The interpretation is useful but must remain tiered:

* `-2 nu s I_s` is the dissipative/restorative part of the finite shell balance;
* `T_s` is internal energy redistribution among retained modes/shells;
* the Genesis phrase "energy = transmitted difference" is an interpretation layer, not an SI-energy derivation.

## 2. Exact transfer--first-jet equivalence

Let `I=(I_1,...,I_m)` and `S=diag(s_1,...,s_m)`. For prescribed forcing,

\[
T=\dot I+2\nu S I-F.
\]

Thus

\[
\begin{bmatrix}I\\T\end{bmatrix}
=
\begin{bmatrix}I_m&0\\2\nu S&I_m\end{bmatrix}
\begin{bmatrix}I\\\dot I\end{bmatrix}
-
\begin{bmatrix}0\\F\end{bmatrix}.
\]

The block matrix has determinant one. Therefore

\[
\boxed{\operatorname{rank}D(I,T)=\operatorname{rank}D(I,\dot I)}.
\]

So the transfer variables do **not** add hidden rank beyond the first Lie block. Their value is structural and numerical: they expose what the scalar total energy cancels, and they permit a derivative-free window formulation.

The exact `K=1` modular checker verifies

\[
\operatorname{rank}D(I,\dot I)=\operatorname{rank}D(I,T)=5,
\]

which is the structural first-block ceiling `3+2=5`, and verifies `sum_s D T_s=0` modulo the good prime used by the existing observability checker.

## 3. Why shell readers beat the total-energy reader

Summing over shells removes the transfer vector:

\[
\frac{d}{dt}\sum_s I_s=-2\nu\sum_ssI_s,
\]

whereas the separate shell equations retain the redistribution pattern `T_s`. This gives a precise mechanism behind the measurement-channel/temporal-depth result in the energy-observability paper: the total reader deliberately collapses internal transfer, while the shell reader keeps it visible.

This explains the structural gain but does not prove all-`N` saturation.

## 4. A constructive all-`N` triad-connectivity lemma

Let

\[
K_N=\{k\in\mathbb Z^3:0<\|k\|_\infty\le N\}.
\]

**Lemma.** For every `N>=2` and every boundary mode `k` with `||k||_infinity=N`, there exist `p in K_{N-1}` and `q in K_N` such that

\[
p+q=k
\]

and `p,q` are non-collinear.

**Construction.** Choose a coordinate `i` with `|k_i|=N`.

1. If `k` has a nonzero transverse component, set `p=sgn(k_i)e_i` and `q=k-p`. Then `p` is in the old cube, `q` stays in the new cube, and the transverse component makes `p` and `q` non-collinear.
2. If `k=+-N e_i` is an axis mode, choose a transverse unit vector `p=e_j`, `j!=i`, and set `q=k-p`. Again `p` is old, `q` is retained, and `p x q !=0`.

For non-collinear `p,q`, suitable divergence-free polarizations make the NS bilinear interaction nonzero. Therefore every newly introduced boundary mode is **kinematically** connected to the previous cutoff. Every newly appearing shell also has a transfer-hypergraph edge to an old shell (indeed to the unit shell under this construction).

The checker exhaustively validates the constructive witness through `N=8`.

**Boundary:** this is not `PROP-NSOBS-07`. Connectivity is necessary structural support, not sufficient algebraic independence. The all-resolution saturation problem is now narrower: show that enough transfer-generated observation rows remain generically independent after the three translation directions are quotiented out.

## 5. Quantitative EPSC-18 witness on the exact triad subcase

The existing analytic three-mode subcase has reduced invariants `(x,y,z,r)` and

\[
c_a=\frac{3}{10},\qquad |a|^2=1,
\]

with

\[
J_{1,a}=2c_a r-2\nu x.
\]

Hence

\[
\boxed{r=\frac{J_{1,a}+2\nu x}{2c_a}}.
\]

If `x` and `J_{1,a}` are known with certified absolute radii `sigma_x` and `sigma_J`, then

\[
\boxed{
|r-\widehat r|
\le
\frac{\sigma_J+2\nu\sigma_x}{2|c_a|}.
}
\]

At `nu=1/200`,

\[
|r-\widehat r|\le\frac53\sigma_J+\frac1{60}\sigma_x.
\]

This is a genuine quantitative inner-inverse certificate for the reduced triad state. It is a **partial witness** for `PROP-EPSC-18`, not closure of the full `N=1` cube or arbitrary `N`.

## 6. A derivative-free EPSC-19 substep

Integrating the shell balance gives

\[
\boxed{
\int_{t_0}^{t_1}T_sdt
=I_s(t_1)-I_s(t_0)+2\nu s\int_{t_0}^{t_1}I_sdt-\int_{t_0}^{t_1}F_sdt.
}
\]

If the four terms on the right have certified radii `r_1,r_0,r_I,r_F`, interval arithmetic gives

\[
\boxed{
\operatorname{rad}\!\left(\int T_sdt\right)
\le r_1+r_0+2\nu s r_I+r_F.
}
\]

This removes numerical differentiation from the transfer-observation substep. It therefore closes one avoidable noise-amplification mechanism inside `PROP-EPSC-19`.

It does **not** yet propagate those transfer intervals through a globally/locally certified full Fourier-state inverse. `PROP-EPSC-19` remains open at that later stage.

## 7. Updated frontier decomposition

What is now closed or reduced:

* exact shell transfer/dissipation separation in the declared finite system;
* exact `(I,T)` versus `(I,dI/dt)` local-rank equivalence;
* all-`N` kinematic boundary-to-old-cutoff triad connectivity;
* quantitative inverse radius in the existing analytic triad reduced model;
* derivative-free window transfer with direct uncertainty-radius propagation.

What remains genuinely open:

* **EPSC-18 full finite quotient inverse:** choose/fix a translation gauge, select an observation branch, and certify conditioning/inversion radius `rho_N` for the full Fourier state;
* **EPSC-19 full noisy inverse:** propagate measured window uncertainty through that certified full inverse and then through EPSC-17;
* **NSOBS-07:** prove/refute generic earliest-order saturation at every finite `N`; after this note, missing triad connectivity is no longer the obstruction, but nonzero-minor/algebraic independence still is;
* **EPSC-16:** make the independent outer certificate tight and scalable at high cutoff/horizon.

The end-to-end target is unchanged:

\[
\text{measured shell-energy windows}
\to(\widehat x_N,\rho_N)
\to\beta_N
\to\sqrt{\rho_N^2+\beta_N^2}
\le\varepsilon.
\]

Until both `rho_N` and `beta_N` are certified, the correct end-to-end verdict remains `HOLD`.
