# Exact K=2 energy observability

## Result

For the cubic Fourier--Galerkin truncation

\[
K_2=\{-2,-1,0,1,2\}^3\setminus\{0\},
\]

there are 124 nonzero Fourier modes and

\[
\boxed{d_2=248}
\]

real divergence-free degrees of freedom. Let

\[
E(x)=\frac12\sum_{k\in K_2}|\widehat u_k|^2
\]

and define the scalar Lie jet

\[
\mathcal E_R=(E,\mathcal L_F E,\ldots,\mathcal L_F^R E).
\]

Spatial translations form a three-dimensional continuous symmetry invisible to `E`, hence

\[
\operatorname{rank}D\mathcal E_R\le d_2-3=245.
\]

Since `E_R` has only `R+1` scalar coordinates,

\[
\operatorname{rank}D\mathcal E_R\le R+1.
\]

Therefore rank 245 is impossible before

\[
\boxed{R=244}.
\]

## Exact modular witness

`checks/check_k2_energy_observability.py` propagates the rational Galerkin Taylor state and 245 projected tangent directions over

\[
\mathbb F_{251}
\]

at `nu=1/200`. The prime is good for this calculation: `251>244`, all fixed Galerkin/basis denominators are invertible, and every factorial through order 244 is invertible. Thus formal Taylor-output blocks and Lie-derivative blocks differ only by invertible row scalings.

The recorded ranks include

\[
\begin{array}{c|cccccccc}
R&10&30&60&120&180&220&243&244\\\hline
\operatorname{rank}&11&31&61&121&181&221&244&245.
\end{array}
\]

In particular, the projected `245 x 245` energy-jet Jacobian has rank 245 at `R=244`. Hence the full `245 x 248` Jacobian has row rank 245 over `F_251`. Therefore some maximal minor of the rational characteristic-zero Jacobian is not identically zero. The translation ceiling supplies the opposite inequality.

### Theorem (K=2 scalar-energy saturation)

At `nu=1/200`,

\[
\boxed{\operatorname{rank}_{\rm gen}D\mathcal E_{244}=245.}
\]

Moreover `R=244` is the earliest mathematically possible order at which rank 245 can occur.

The positive-viscosity scaling conjugacy

\[
F_\nu(\nu y)=\nu^2F_1(y),
\qquad
D_x\mathcal L_{F_\nu}^rE(\nu y)
=\nu^{r+1}D_y\mathcal L_{F_1}^rE(y)
\]

shows that generic rank is independent of the value of every `nu>0`. Consequently

\[
\boxed{
\operatorname{rank}_{\rm gen}D\mathcal E_{244}=245
\qquad\text{for every }\nu>0.
}
\]

At generic states the translation action is free, so the kernel has exactly the three infinitesimal translation directions. This is local observability modulo translation, not global injectivity.

## Cross-check and provenance

The same optimized implementation specialized back to `K=1`, `R=48`, `d=52` reproduces the previously recorded scalar rank pattern

\[
1,2,\ldots,49,
\]

with rank 49 first reached at `R=48` over the same good prime `251`.

Machine-readable K=2 output is stored at

`results/k2_energy_observability_mod251.json`.

The K=2 checker is

`checks/check_k2_energy_observability.py`.

## Updated finite pattern

The energy-readout saturation proposal now has two exact finite resolution points:

\[
\boxed{
K_1:\ 52\to49,\ R_{\min}=48,
\qquad
K_2:\ 248\to245,\ R_{\min}=244.
}
\]

The general statement for every finite `K_N` remains a conjecture. No continuum Navier--Stokes regularity, singularity, global reconstruction, noise stability, or computational speed-up claim is made.
