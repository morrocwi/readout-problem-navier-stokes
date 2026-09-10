# Fixed-N=1 direct raw-sample inverse for EPSC-19 / EPSC-36

## Purpose

This note records the finite-first bridge from raw shell-energy samples directly to a certified local retained-state radius. It deliberately bypasses the numerically hostile route

\[
\text{samples}\to\text{high-order Taylor jet}\to\rho_1.
\]

The domain-specific executable certificate is
`reproduction/checks/check_volume7_eps19_n1_direct_sample_inverse.py`.

## Finite sample map

On the already-certified 49-dimensional translation slice of the `N=1` Fourier-Galerkin system, let `phi_t` denote the finite polynomial Galerkin flow and let `I_0,I_1,I_2` be its three shell energies. Define

\[
\mathcal S_h(x)=
\bigl(I_0(\phi_{jh}(x))\bigr)_{j=0}^{23}
\oplus
\bigl(I_1(\phi_{jh}(x))\bigr)_{j=0}^{23}
\oplus I_2(x).
\]

The proof construction fixes the explicit rational spacing

\[
\boxed{h=10^{-200}}.
\]

This spacing is intentionally microscopic. Its role is to close the mathematical interface with large safety margin, not to claim a practical sensor design.

## Direct preconditioner

Let `a_{s,n}` be the Taylor coefficients of `I_s(phi_t(x))`. The existing full-rank chart is stored in the scaled coordinates

\[
z_{s,n}=600^n n!\,a_{s,n}.
\]

In sample-channel order, its exact characteristic-zero Jacobian is a nonsingular integer matrix `J_z`. The degree-23 direct sample Jacobian is

\[
J_T(h)=P_hJ_z,
\]

where the two 24-row primary-shell blocks of `P_h` are

\[
V\,\operatorname{diag}\!\left(\frac{h^n}{600^n n!}\right)_{n=0}^{23},
\qquad V_{jn}=j^n,
\]

and the final `I_2(x)` row is unchanged. Hence

\[
\boxed{A_h=J_z^{-1}P_h^{-1}}
\]

is an exact rational preconditioner satisfying

\[
A_hJ_T(h)=I
\]

exactly. The factorization is only a proof device used to construct the preconditioner. The certified measurement map itself acts directly on the 49 raw samples; it does not first reconstruct the high-order Taylor jet.

## Finite validation of the actual sample map

All validation is carried out on a fixed finite state-space box. The checker uses finite operator bounds for

\[
\dot x=Lx+B(x,x)
\]

and integral bootstrap inequalities over the complete interval `0 <= t <= 23h` to certify a state bound, a tangent bound for `D phi_t`, and a second-variation bound for `D^2 phi_t`.

The difference between the actual center Jacobian `D S_h(x_*)` and the degree-23 polynomial Jacobian `J_T(h)` is bounded with the ordinary finite 24th-order Taylor theorem. This requires only a bound on the 24th time derivative over the finite interval. It does not require an infinite Taylor series.

Likewise, the exact center sample values are represented by a degree-47 rational Taylor polynomial `y_T`; the actual center sample vector lies in a certified finite remainder box obtained from the 48th-order Taylor theorem.

## Branch-wide inverse gate

Let `e_j` be the certified center-Jacobian remainder of sample row `j`, and let `H_j` bound the row Hessian of the actual finite sample map throughout a branch `B_r(x_*)`. Then

\[
q\le
\max_i\sum_j |(A_h)_{ij}|\,(e_j+rH_j).
\]

The executable checker chooses a strictly positive `r` for which

\[
\boxed{q\le\tfrac12<1}.
\]

Consequently the direct raw-sample map is quantitatively invertible on that certified local branch.

## Raw-data branch capture

Let `y_obs` be a 49-vector of raw measured shell-energy samples with certified sup-norm sensor radius `sigma`. Let `y_T` be the exact degree-47 center polynomial and `tau_T` its validated flow remainder. If

\[
\|y_{obs}-y_T\|_\infty+\sigma+\tau_T
\le
\frac{(1-q)r}{\|A_h\|_\infty},
\]

then for every data vector `y` in the declared measurement box the map

\[
T_y(x)=x-A_h(\mathcal S_h(x)-y)
\]

is a contraction mapping the branch into itself. Banach's theorem therefore certifies a unique root in that local branch, without assuming branch membership in advance. Moreover

\[
\boxed{
\|x-x_*\|_\infty
\le
\frac{\|A_h\|_\infty}{1-q}
\bigl(\|y_{obs}-y_T\|_\infty+\sigma+\tau_T\bigr).
}
\]

Thus, once the executable inequalities pass, the fixed-`N=1` chain is genuinely

\[
\boxed{
\text{raw finite time samples}
\longrightarrow
\text{certified local branch}
\longrightarrow
\rho_1.
}
\]

## Claim boundary

This closes only the *mathematical fixed-`N=1` local measurement interface* if the checker passes. The declared `h=10^-200` and the resulting admissible sample tolerance are expected to be far too small for physical sensors. Practical schedule optimization remains separate. Global injectivity, arbitrary finite `N`, the outer `beta_N` scaling problem, physical DNS adequacy, continuum regularity, and the Clay Millennium problem are not implied.

The construction is finite-first throughout: 52 finite state coordinates, a 49-dimensional finite quotient slice, 49 finite samples, finite Taylor orders 24 and 48, and rational contraction inequalities. No completed `N=infinity` Fourier object is a premise.
