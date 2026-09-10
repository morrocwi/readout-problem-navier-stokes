# Row-aware quantitative inverse radius for the full N=1 finite energy-observability chart

**Status:** post-paper EPSC analytic note.  This note concerns a fixed finite Fourier-Galerkin system only.  It is not a continuum-regularity theorem and it does not solve the Clay Navier-Stokes problem.

## 1. Setting

Use the periodic `N=1` Fourier-Galerkin state already fixed by the energy-observability lane.  The real divergence-free state dimension is 52.  The shell-energy reader is invariant under the three-dimensional spatial-translation action, and the reproduced finite calculation supplies an explicit translation-transverse affine coordinate slice of dimension 49 together with 49 selected shell-energy Taylor observations.

After the exact row scaling used by the finite checker, let

\[
H:\mathbb R^{49}\to\mathbb R^{49},
\qquad
J(x)=DH(x),
\qquad
J_0=J(x_*),
\]

where `x_*` is the deterministic small-integer center with `max_j |x_{*,j}|=3`.  The selected scaled center matrix `J_0` is an integer matrix and the good-prime calculation certifies that its determinant is nonzero.  Consequently

\[
|\det J_0|\ge 1.
\]

This integer lower bound is the only determinant-size information used below.

## 2. Row-wise finite majorants

For selected observation row `j`, let

\[
R_j\ge \|J_{0,j*}\|_1
\]

be a certified finite row majorant at the center.  On the infinity-norm box containing the radius under consideration, let

\[
H_j\ge
\sup_x \|D(J_{j*})(x)\|_{\infty\to 1}
\]

be a certified row-variation majorant.  The reproduction implementation obtains these from the same finite polynomial Galerkin recurrence used in the preceding conservative-radius checker, but it retains the Taylor-order dependence rather than replacing every row by one global maximum.

For a point satisfying `||x-x_*||_infinity <= r`, the mean-value estimate gives

\[
\|J_{j*}(x)-J_{0,j*}\|_1\le H_j r.
\]

## 3. Row-aware cofactor estimate

Define

\[
C_j:=\prod_{k\ne j}R_k.
\]

Every cofactor in column `j` of `J_0^{-1}` is the determinant of a 48-by-48 matrix formed by deleting observation row `j`.  Hadamard's inequality and the row bounds give

\[
|\operatorname{cof}_{j i}(J_0)|
\le C_j.
\]

Because `|det J_0|>=1`, Cramer's formula yields

\[
|(J_0^{-1})_{i j}|\le C_j.
\]

Therefore, for every row `i`,

\[
\begin{aligned}
\sum_\ell
\left|
\bigl[J_0^{-1}(J(x)-J_0)\bigr]_{i\ell}
\right|
&\le
\sum_j |(J_0^{-1})_{ij}|\,
\|J_{j*}(x)-J_{0,j*}\|_1\\
&\le
r\sum_j C_jH_j.
\end{aligned}
\]

Taking the maximum over `i` gives the finite quantitative theorem

\[
\boxed{
\|J_0^{-1}(J(x)-J_0)\|_\infty
\le
r\sum_{j=1}^{49}
\left(\prod_{k\ne j}R_k\right)H_j.
}
\]

Hence the explicit choice

\[
\boxed{
 r_{\rm row}
 =
 \frac{1}{
 2\sum_{j=1}^{49}
 (\prod_{k\ne j}R_k)H_j
 }
}
\]

certifies

\[
\|J_0^{-1}(J(x)-J_0)\|_\infty\le\frac12<1.
\]

Thus the same local branch has a strictly positive quantitative inverse radius.

## 4. Reproduced magnitude

The earlier uniform-row Cramer/Hadamard construction used the largest Jacobian-row majorant and largest Hessian-row majorant for all 49 rows.  Its denominator had 7934 decimal digits, giving

\[
10^{-7934}<r_{\rm uniform}\le10^{-7933}.
\]

The row-aware construction has a denominator with 3878 decimal digits and therefore gives

\[
\boxed{
10^{-3878}<r_{\rm row}\le10^{-3877}.
}
\]

The power-of-ten lower-bound bracket improves by 4056 decimal orders.  The row-aware cofactor infinity-bound used in the construction has 3871 decimal digits.

These are not floating estimates of the true conditioning.  They are conservative finite certificates obtained from integer/rational inequalities.

## 5. What this closes and what remains open

This result closes the following narrow statement at the fixed full `N=1` finite resolution:

> there is an explicit, strictly positive, quantitatively certified neighborhood on the 49-dimensional symmetry slice on which the selected energy-jet chart has a controlled local inverse.

It does **not** show that the radius is useful for experimental measurements.  Even after removing more than four thousand orders of avoidable uniform-row slack, `10^-3878` remains astronomically below any practical sensor tolerance.

The next mathematically relevant step is therefore not another global determinant bound.  It is to construct the actual characteristic-zero selected Jacobian, choose an effective rational approximate inverse/preconditioner `A`, build an entrywise certified interval enclosure `J(B)`, and verify fail-closed

\[
q=\|I-AJ(B)\|_\infty<1.
\]

Then observation uncertainty can be converted to a retained-state radius by

\[
\rho_1
\le
\frac{\|A\|_\infty}{1-q}
(\sigma_{\rm meas}+\sigma_{\rm res}),
\]

provided the common branch/symmetry-slice containment is independently certified.

## 6. Reproduction and provenance

Executable source:

- `reproduction/checks/check_volume7_eps18_n1_local_inverse.py`
- `reproduction/checks/check_volume7_eps18_n1_small_witness.py`
- `reproduction/checks/check_volume7_eps18_n1_explicit_radius.py`
- `reproduction/checks/check_volume7_eps18_n1_rowwise_radius.py`

The generated reproduction ledger records the local inverse, the original positive radius, the row-aware tightening, and the still-open practical preconditioned radius separately.

Toledo provenance uses proposal identifiers `PROP-EPSC-22..26`.  These are proposal records, not canonical verified Toledo theorem codes.

## 7. Claim boundary

No statement here implies global injectivity of the energy reader, arbitrary-`N` inversion, noise-stable reconstruction from real measurements, equality of a finite Galerkin path with a continuum solution, global regularity or finite-time singularity of three-dimensional Navier-Stokes, physical turbulent-DNS adequacy, or a resolution of the Clay Millennium problem.
