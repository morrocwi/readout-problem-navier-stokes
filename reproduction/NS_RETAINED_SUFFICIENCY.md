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

The next mathematical target is not a new dynamical law. It is a richer retained map

\[
R(u)=\bigl(I(u),\Xi(u)\bigr)
\]

such that

\[
R(u)=R(v)
\Longrightarrow
\eta^{\mathrm{NS}}(u)=\eta^{\mathrm{NS}}(v),
\]

with \(\Xi\) restricted to distinctions forced by the nonlinear triad structure.
