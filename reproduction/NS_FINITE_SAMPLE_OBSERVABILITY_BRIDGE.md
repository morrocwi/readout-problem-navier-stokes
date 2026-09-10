# Finite-time sample observability bridge at fixed N=1

Status: post-paper finite-first research note. This note advances the measurement side of EPSC-19 without claiming raw-sensor branch capture or continuum Navier--Stokes regularity.

## 1. Starting point

For the finite `N=1` Fourier--Galerkin system, the real state dimension is 52. Spatial translations give a three-dimensional symmetry, and the existing exact witness fixes a transverse three-coordinate gauge, leaving a 49-dimensional slice `S_1`.

At the deterministic small-integer center `x_*`, the shell-energy Taylor observation coefficients

\[
I_s(\phi_t(x))=\sum_{n\ge0} a_{s,n}(x)t^n
\]

have a nonsingular 49-row Jacobian on that slice. The selected row pattern is

\[
(s,n)=(0,0),(1,0),(2,0),
\]

together with

\[
(s,n)=(0,n),(1,n),\qquad n=1,\ldots,23.
\]

This is the structural chart already used by the fixed-`N=1` EPSC-18 certificate chain.

## 2. Replace derivatives by actual finite-time samples

Define the 49-component sample map

\[
\mathcal S_h(x)=
\Bigl(
I_0(\phi_{0h}(x)),\ldots,I_0(\phi_{23h}(x)),
I_1(\phi_{0h}(x)),\ldots,I_1(\phi_{23h}(x)),
I_2(x)
\Bigr).
\]

No numerical derivative appears in this definition. It consists only of shell-energy values at 24 finite sample times for two shells plus the third shell at time zero.

Because the finite Galerkin vector field is polynomial, its local flow and the composed shell-energy outputs are analytic in time around the declared finite center. Hence

\[
D_x I_s(\phi_{jh}(x_*))
=\sum_{n\ge0}j^n h^n D a_{s,n}(x_*).
\]

## 3. Determinant leading term

For one shell, the 24 sample rows at `j=0,...,23` are related at leading orders to the first 24 Taylor rows by the Vandermonde matrix

\[
V_{jn}=j^n,\qquad 0\le j,n\le23.
\]

The nodes are distinct, so

\[
\det V=\prod_{0\le i<j\le23}(j-i)\ne0.
\]

There are two such 24-row shell blocks. The least possible total power of `h` in a nonzero determinant term is therefore

\[
2\sum_{n=0}^{23}n=2\cdot276=552.
\]

Let `J_jet` denote the same 49 Taylor rows, reordered as shell 0 orders `0..23`, shell 1 orders `0..23`, and shell 2 order 0. Then

\[
\boxed{
\det D\mathcal S_h(x_*)
= c\,h^{552}+O(h^{553}),
\qquad
c=(\det V)^2\det J_{\rm jet}\ne0.
}
\]

The companion checker verifies the two finite algebraic nonvanishing factors modulo the good prime `p=1000003`. Since the relevant rational/integer denominators are invertible at that prime, the good-prime nonvanishing certifies characteristic-zero nonvanishing of the underlying finite coefficient.

Therefore there exists some `eta>0` such that

\[
0<|h|<\eta
\quad\Longrightarrow\quad
\det D\mathcal S_h(x_*)\ne0.
\]

By the ordinary finite-dimensional inverse-function theorem, `S_h` is a local chart on the same 49-dimensional quotient slice for every sufficiently small nonzero sample spacing.

## 4. What this changes

The structural measurement chain can now be written

\[
\boxed{
\text{finite shell-energy values at finitely many times}
\longrightarrow
\text{local quotient observability}
}
\]

without reconstructing 23 time derivatives from noisy data first.

This is a meaningful narrowing of the EPSC-19 measurement frontier: high-order numerical differentiation is no longer structurally necessary at fixed `N=1`.

## 5. What remains open

The result is intentionally existential in the sample spacing. It does **not** yet provide:

- an explicit useful value or interval for `h`;
- a branch-wide interval enclosure for `D S_h`;
- a certified preconditioner with `q_h<1` on a nonzero branch box;
- a useful noise-to-state factor for raw samples;
- a theorem that noisy raw measurements select the correct local branch;
- arbitrary-finite-`N` sample-chart conditioning;
- a continuum omitted-tail certificate for any particular experiment.

Those are the next quantitative obligations. In particular, taking `h` arbitrarily small is not automatically good numerically: the Vandermonde structure becomes increasingly ill-conditioned even though local invertibility is guaranteed. A practical certificate must balance sample spacing, finite-flow/Taylor remainder, conditioning, measurement noise and branch containment.

## 6. Claim boundary

This is a theorem about one fixed finite polynomial Galerkin system and its local quotient observation map. It does not establish global injectivity, physical sensor adequacy, DNS convergence, continuum Navier--Stokes regularity or blow-up, and it does not solve the Clay Millennium problem.
