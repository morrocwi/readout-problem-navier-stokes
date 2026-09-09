# Retained-State Sufficiency Test

Let

\[
I(u)=\bigl(I_1(u),\ldots,I_m(u)\bigr)
\]

with

\[
I_j(u)
=
\frac12\sum_{|k|^2=q_j}|\widehat u_k|^2,
\]

and let

\[
\eta^{\mathrm{NS}}(u)
=
\bigl(T_1(u),\ldots,T_m(u)\bigr)
\]

be the nonlinear tape read directly from the projected Navier--Stokes term.

The autonomy condition

\[
\eta^{\mathrm{NS}}=\Gamma(I)
\]

requires

\[
I(u)=I(v)
\Longrightarrow
\eta^{\mathrm{NS}}(u)=\eta^{\mathrm{NS}}(v).
\]

Construct two divergence-free, conjugate-symmetric, 2/3-dealiased finite Fourier states
\(u^{(A)}\) and \(u^{(B)}\). Rescale \(u^{(B)}\) shell-by-shell so that

\[
I_j\bigl(u^{(A)}\bigr)
=
I_j\bigl(u^{(B)}\bigr)
\qquad\forall j.
\]

The deterministic finite check gives

\[
\max_j
\left|
I_j\bigl(u^{(A)}\bigr)
-I_j\bigl(u^{(B)}\bigr)
\right|
=
1.734723475976807\times10^{-18},
\]

but

\[
\frac{
\left\|
\eta^{\mathrm{NS}}\bigl(u^{(A)}\bigr)
-
\eta^{\mathrm{NS}}\bigl(u^{(B)}\bigr)
\right\|
}{
\left\|
\eta^{\mathrm{NS}}\bigl(u^{(A)}\bigr)
\right\|
}
=
1.4125123742534211.
\]

Also

\[
\left|\sum_j\eta_j^{\mathrm{NS}}\bigl(u^{(A)}\bigr)\right|
=1.2468324983583301\times10^{-18},
\]

\[
\left|\sum_j\eta_j^{\mathrm{NS}}\bigl(u^{(B)}\bigr)\right|
=1.548376227580861\times10^{-18}.
\]

Therefore the finite witness satisfies

\[
I\bigl(u^{(A)}\bigr)
\approx
I\bigl(u^{(B)}\bigr),
\qquad
\eta^{\mathrm{NS}}\bigl(u^{(A)}\bigr)
\neq
\eta^{\mathrm{NS}}\bigl(u^{(B)}\bigr).
\]

Hence shell energy alone is not an exact sufficient retained state for the nonlinear tape:

\[
\boxed{
\nexists\,\Gamma
\text{ such that }
\eta^{\mathrm{NS}}(u)=\Gamma(I(u))
\text{ on the whole tested finite state class.}
}
\]

## Resolution of the richer-state target

The earlier working target

\[
R(u)=\bigl(I(u),\Xi(u)\bigr)
\]

is superseded.  Readout Genesis already reserves \(\Xi_n\) for its
`orientation_selecting_order` slot, so the richer Navier--Stokes state is not assigned
that symbol.

The canonical exact object is now the future-shell-readout quotient

\[
\boxed{
\mathcal Q_{\min}^{NS}
=
X_M/\!\sim_I,
\qquad
x\sim_Iy
\iff
I(\Phi_t x)=I(\Phi_t y)
\ \forall t\ge0.
}
\]

`NS_MINIMAL_DYNAMIC_READOUT.md` proves the quotient universal property and, for every
fixed finite polynomial Galerkin truncation, proves existence of a finite Lie-readout jet

\[
\boxed{
(J_0,\ldots,J_{R_M^\star}),
\qquad
J_0=I,
\quad
J_{r+1}=\mathcal L_{F_M}J_r,
}
\]

with exactly the same fibers as \(\mathcal Q_{\min}^{NS}\).

The first nontrivial jet level is forced by Navier--Stokes triads:

\[
J_1
=
-L_\nu I+\eta^{NS}.
\]

Thus the finite exact **state-sufficiency target is closed**.  What remains open is the
computational target: determine \(R_M^\star\), remove redundant jet coordinates, and show
that evolving the resulting quotient is materially cheaper than the full 3D Galerkin
system at useful resolution.
