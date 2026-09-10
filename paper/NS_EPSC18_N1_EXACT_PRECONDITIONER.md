# Exact characteristic-zero preconditioning for the full N=1 finite energy-observability chart

**Status:** post-paper EPSC analytic note with executable finite reproduction. This note concerns one fixed finite Fourier-Galerkin system. It is not a continuum-regularity theorem, a physical-DNS validation, or a solution of the Clay Navier-Stokes problem.

## 1. Why the previous radius was still tiny

The full `N=1` shell-energy observability chart has 52 real Fourier-Galerkin coordinates. Spatial translation contributes three unavoidable reader symmetries, and the reproduced construction fixes a transverse three-coordinate gauge, leaving a 49-dimensional slice. A selected set of 49 shell-energy Taylor observations gives a square local chart

\[
H:\mathbb R^{49}\to\mathbb R^{49},\qquad J(x)=DH(x).
\]

Earlier certificates already proved that an explicit small-integer center `x_*` has an invertible selected Jacobian and then produced strictly positive radii. The first uniform Cramer/Hadamard bound gave

\[
10^{-7934}<r_{\rm uniform}\le10^{-7933},
\]

and the row-aware cofactor refinement improved this to

\[
10^{-3878}<r_{\rm row}\le10^{-3877}.
\]

Those estimates were rigorous, but their small size mainly reflected determinant/cofactor upper bounds rather than the actual conditioning of the selected matrix.

## 2. Reconstruct the actual characteristic-zero Jacobian

Let `C=600`. For Taylor order `n`, multiply the selected shell-energy Jacobian row by the exact factor

\[
C^n n!.
\]

For the declared `N=1`, `nu=1/200` Galerkin system this clears the finite coordinate-extraction and viscosity denominators used by the recurrence. The checker therefore constructs an integer matrix

\[
J_0=J(x_*)\in\mathbb Z^{49\times49}
\]

in the scaled observation coordinates.

The characteristic-zero construction is not accepted merely because it is numerically nonsingular. Every one of the 49 selected rows is reduced modulo the good prime

\[
p=1,000,003
\]

and compared with the independent exact modular Taylor-jet construction after the same `C^n n!` scaling. The determinant is also reduced modulo `p` and cross-checked against the previously certified modular minor with the accumulated row-scale factor.

The reproduction pass certifies both checks. The resulting nonzero integer determinant has **2561 decimal digits**. The exact determinant value itself is not needed for the theorem; its nonvanishing and the cross-check are the relevant facts.

## 3. Exact rational inverse

Instead of applying Cramer's inequality to `J_0`, invert the actual matrix by exact rational Gauss-Jordan elimination:

\[
A:=J_0^{-1}\in\mathbb Q^{49\times49}.
\]

There is no floating inversion in the certificate. The induced infinity norm is computed exactly as a rational maximum row sum, and the checker certifies the simple rational bracket

\[
\boxed{
1.28<\|J_0^{-1}\|_\infty<1.29.
}
\]

This explains why the previous determinant-based radii were so pessimistic: the actual selected center matrix is not remotely conditioned at the `10^{3870}` scale suggested by the row-aware cofactor upper bound.

## 4. Exact-preconditioned local radius

For selected observation row `j`, let `H_j` be the already-certified finite upper bound on the row variation per unit infinity-radius on the declared enclosing box. Set

\[
S=\max_i\sum_{j=1}^{49}|A_{ij}|H_j.
\]

For every `x` on the same symmetry slice with `||x-x_*||_infinity<=r`, the mean-value estimate gives

\[
\|A(J(x)-J_0)\|_\infty\le rS.
\]

Because `A=J_0^{-1}` exactly, the preconditioned center defect is zero. Hence the explicit choice

\[
\boxed{
r_{\rm exact}=\frac{1}{2S}
}
\]

certifies

\[
\boxed{
\|J_0^{-1}(J(x)-J_0)\|_\infty\le\frac12<1.
}
\]

The executable finite checker gives the reproduced power-of-ten bracket

\[
\boxed{
10^{-59}<r_{\rm exact}\le10^{-58}.
}
\]

Thus the progression of rigorous lower-bracket scales is

\[
10^{-7934}
\;\longrightarrow\;
10^{-3878}
\;\longrightarrow\;
10^{-59}.
\]

The improvement does not come from weakening the theorem. It comes from replacing an intentionally coarse determinant/cofactor surrogate by the actual characteristic-zero finite inverse.

## 5. What is now established

At the fixed full `N=1` finite resolution, the programme now has all of the following on one explicit translation-transverse 49-dimensional chart:

- exact modular rank saturation and a nonzero selected minor;
- a characteristic-zero integer reconstruction of that selected Jacobian;
- modular cross-check of all selected characteristic-zero rows;
- exact rational inversion of the 49-by-49 center Jacobian;
- an exact inverse-norm bracket `1.28 < ||J0^-1||_inf < 1.29`;
- a strictly positive exact-preconditioned local radius with `q<=1/2` and `10^-59 < r <= 10^-58`.

This closes another finite conditioning obligation. It does not yet make the inverse measurement-ready.

## 6. The remaining source of large slack

After exact preconditioning, determinant inflation is no longer the dominant problem. The remaining `10^-59` scale is driven by conservative Jacobian/Hessian variation majorants propagated through the nonlinear Taylor recurrence.

The next useful refinement is therefore **componentwise finite majorization**: construct the exact coefficient tensor of the scaled quadratic Galerkin map and propagate coordinatewise state, first-derivative, and second-derivative bounds instead of collapsing the entire recurrence to one scalar operator maximum. An even tighter later stage can use a genuinely entrywise interval Jacobian around the center.

The target fail-closed structure remains

\[
q=\|I-AJ(B)\|_\infty<1,
\]

followed, only with independently certified branch/symmetry containment, by

\[
\rho_1\le
\frac{\|A\|_\infty}{1-q}
(\sigma_{\rm meas}+\sigma_{\rm res}).
\]

A mathematically positive state-space radius is not automatically a practical sensor tolerance.

## 7. Reproduction and provenance

Executable source:

- `reproduction/checks/check_volume7_eps18_n1_local_inverse.py`
- `reproduction/checks/check_volume7_eps18_n1_small_witness.py`
- `reproduction/checks/check_volume7_eps18_n1_explicit_radius.py`
- `reproduction/checks/check_volume7_eps18_n1_rowwise_radius.py`
- `reproduction/checks/check_volume7_eps18_n1_exact_preconditioner.py`

The full reproduction workflow passed after the exact-preconditioner checker was added. Toledo records this result as proposal identifier `PROP-EPSC-27`; it remains a proposal/provenance record rather than a canonical verified Toledo theorem code.

## 8. Claim boundary

Nothing in this note establishes global injectivity of shell-energy histories, robust branch selection under real measurement noise, arbitrary-`N` inversion, all-resolution observability saturation, equality of a finite Galerkin trajectory with the continuum solution, global regularity or finite-time singularity of three-dimensional Navier-Stokes, turbulent-DNS adequacy, or a resolution of the Clay Millennium problem.
